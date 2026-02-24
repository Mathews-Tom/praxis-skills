#!/usr/bin/env python3
"""
Lightweight code complexity analyzer.
Produces a JSON report of per-function complexity metrics for Python, Go, TS/JS files.
No external dependencies — uses AST parsing for Python, regex heuristics for others.

Usage:
    python complexity_report.py <file_or_directory> [--format json|markdown]
"""

from __future__ import annotations

import ast
import json
import os
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class FunctionMetrics:
    file: str
    name: str
    line_start: int
    line_end: int
    lines_of_code: int
    max_nesting_depth: int
    branch_count: int  # if/elif/else/match/case/for/while/try/except
    parameter_count: int
    return_count: int
    cognitive_complexity: int  # simplified cognitive complexity score


@dataclass
class FileReport:
    file: str
    language: str
    total_lines: int
    functions: list
    dead_imports: list  # Python only


# ---------------------------------------------------------------------------
# Python analysis (AST-based, precise)
# ---------------------------------------------------------------------------

class PythonAnalyzer(ast.NodeVisitor):
    def __init__(self, source: str, filepath: str):
        self.source = source
        self.filepath = filepath
        self.functions: list[FunctionMetrics] = []
        self.imports: set[str] = set()
        self.used_names: set[str] = set()
        self._lines = source.splitlines()

    def analyze(self) -> FileReport:
        tree = ast.parse(self.source)
        self.visit(tree)
        # Detect potentially unused imports (heuristic)
        dead = sorted(self.imports - self.used_names)
        return FileReport(
            file=self.filepath,
            language="python",
            total_lines=len(self._lines),
            functions=[asdict(f) for f in self.functions],
            dead_imports=dead,
        )

    def visit_Import(self, node):
        for alias in node.names:
            name = alias.asname or alias.name.split(".")[0]
            self.imports.add(name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            name = alias.asname or alias.name
            self.imports.add(name)
        self.generic_visit(node)

    def visit_Name(self, node):
        self.used_names.add(node.id)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self._analyze_function(node)

    def visit_AsyncFunctionDef(self, node):
        self._analyze_function(node)

    def _analyze_function(self, node):
        metrics = FunctionMetrics(
            file=self.filepath,
            name=node.name,
            line_start=node.lineno,
            line_end=node.end_lineno or node.lineno,
            lines_of_code=(node.end_lineno or node.lineno) - node.lineno + 1,
            max_nesting_depth=self._max_nesting(node),
            branch_count=self._count_branches(node),
            parameter_count=len(node.args.args) + len(node.args.kwonlyargs),
            return_count=self._count_returns(node),
            cognitive_complexity=self._cognitive_complexity(node),
        )
        self.functions.append(metrics)
        self.generic_visit(node)

    def _max_nesting(self, node, depth=0) -> int:
        max_d = depth
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.With, ast.Try,
                                  ast.ExceptHandler, ast.Match)):
                child_depth = self._nesting_depth_of(child, node)
                max_d = max(max_d, child_depth)
        return max_d

    def _nesting_depth_of(self, target, root) -> int:
        """Count nesting depth of target relative to root."""
        nesting_types = (ast.If, ast.For, ast.While, ast.With, ast.Try,
                         ast.ExceptHandler, ast.Match, ast.FunctionDef,
                         ast.AsyncFunctionDef)
        depth = 0
        for node in ast.walk(root):
            if node is target:
                return depth
            if isinstance(node, nesting_types) and node is not root:
                depth += 1
        return depth

    def _count_branches(self, node) -> int:
        count = 0
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.Try,
                                  ast.ExceptHandler, ast.Match)):
                count += 1
        return count

    def _count_returns(self, node) -> int:
        return sum(1 for child in ast.walk(node) if isinstance(child, ast.Return))

    def _cognitive_complexity(self, node, nesting=0) -> int:
        """Simplified cognitive complexity: +1 per branch, +nesting for nested branches."""
        total = 0
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.If, ast.For, ast.While)):
                total += 1 + nesting
                total += self._cognitive_complexity(child, nesting + 1)
            elif isinstance(child, (ast.Try, ast.ExceptHandler)):
                total += 1 + nesting
                total += self._cognitive_complexity(child, nesting + 1)
            elif isinstance(child, ast.BoolOp):
                total += 1  # each and/or adds +1
                total += self._cognitive_complexity(child, nesting)
            else:
                total += self._cognitive_complexity(child, nesting)
        return total


# ---------------------------------------------------------------------------
# Generic analysis (regex-based heuristic for Go, TS, JS, Rust)
# ---------------------------------------------------------------------------

FUNC_PATTERNS = {
    "go": re.compile(r"^func\s+(?:\([^)]*\)\s+)?(\w+)\s*\(([^)]*)\)"),
    "typescript": re.compile(r"(?:export\s+)?(?:async\s+)?function\s+(\w+)\s*\(([^)]*)\)"),
    "javascript": re.compile(r"(?:export\s+)?(?:async\s+)?function\s+(\w+)\s*\(([^)]*)\)"),
    "rust": re.compile(r"(?:pub\s+)?(?:async\s+)?fn\s+(\w+)\s*(?:<[^>]*>)?\s*\(([^)]*)\)"),
}

BRANCH_KEYWORDS = re.compile(r"\b(if|else if|elif|else|for|while|match|switch|case|try|catch|except)\b")


def analyze_generic(source: str, filepath: str, language: str) -> FileReport:
    lines = source.splitlines()
    functions: list[FunctionMetrics] = []
    pattern = FUNC_PATTERNS.get(language)

    if pattern:
        i = 0
        while i < len(lines):
            m = pattern.match(lines[i].strip())
            if m:
                name = m.group(1)
                params = m.group(2).strip()
                param_count = len([p for p in params.split(",") if p.strip()]) if params else 0
                start = i + 1
                # Find function end by brace counting
                end = _find_block_end(lines, i)
                block = lines[i:end]
                block_str = "\n".join(block)

                branches = len(BRANCH_KEYWORDS.findall(block_str))
                max_nest = _estimate_max_nesting(block)
                returns = block_str.count("return ")

                functions.append(asdict(FunctionMetrics(
                    file=filepath,
                    name=name,
                    line_start=start,
                    line_end=end,
                    lines_of_code=end - i,
                    max_nesting_depth=max_nest,
                    branch_count=branches,
                    parameter_count=param_count,
                    return_count=returns,
                    cognitive_complexity=branches + max_nest,  # rough estimate
                )))
                i = end
            else:
                i += 1

    return FileReport(
        file=filepath,
        language=language,
        total_lines=len(lines),
        functions=functions,
        dead_imports=[],
    )


def _find_block_end(lines: list[str], start: int) -> int:
    depth = 0
    for i in range(start, len(lines)):
        depth += lines[i].count("{") - lines[i].count("}")
        if depth <= 0 and i > start:
            return i + 1
    return len(lines)


def _estimate_max_nesting(block: list[str]) -> int:
    """Estimate max nesting by indentation delta."""
    if not block:
        return 0
    base_indent = len(block[0]) - len(block[0].lstrip())
    max_depth = 0
    for line in block:
        if line.strip():
            indent = len(line) - len(line.lstrip())
            depth = max(0, (indent - base_indent) // 4)  # assume 4-space or tab
            max_depth = max(max_depth, depth)
    return max_depth


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

LANG_MAP = {
    ".py": "python",
    ".go": "go",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".js": "javascript",
    ".jsx": "javascript",
    ".rs": "rust",
}


def analyze_file(filepath: str) -> FileReport | None:
    path = Path(filepath)
    lang = LANG_MAP.get(path.suffix)
    if not lang:
        return None

    source = path.read_text(encoding="utf-8", errors="replace")

    if lang == "python":
        try:
            return PythonAnalyzer(source, filepath).analyze()
        except SyntaxError:
            return None
    else:
        return analyze_generic(source, filepath, lang)


def analyze_path(target: str) -> list[dict]:
    target_path = Path(target)
    reports = []

    if target_path.is_file():
        report = analyze_file(str(target_path))
        if report:
            reports.append(asdict(report))
    elif target_path.is_dir():
        for root, dirs, files in os.walk(target_path):
            # Skip hidden dirs and common non-source dirs
            dirs[:] = [d for d in dirs if not d.startswith(".")
                       and d not in ("node_modules", "vendor", "__pycache__", "target", ".git")]
            for f in sorted(files):
                fpath = os.path.join(root, f)
                report = analyze_file(fpath)
                if report:
                    reports.append(asdict(report))

    return reports


def format_markdown(reports: list[dict]) -> str:
    lines = ["# Complexity Report\n"]
    for r in reports:
        lines.append(f"## {r['file']} ({r['language']}, {r['total_lines']} lines)\n")
        if r["dead_imports"]:
            lines.append(f"⚠️  Potentially unused imports: {', '.join(r['dead_imports'])}\n")
        if r["functions"]:
            lines.append("| Function | Lines | Nesting | Branches | Params | Cognitive |")
            lines.append("|----------|-------|---------|----------|--------|-----------|")
            for f in r["functions"]:
                flag = " ⚠️" if f["cognitive_complexity"] > 10 or f["max_nesting_depth"] > 3 else ""
                lines.append(
                    f"| `{f['name']}` | {f['lines_of_code']} | {f['max_nesting_depth']} | "
                    f"{f['branch_count']} | {f['parameter_count']} | {f['cognitive_complexity']}{flag} |"
                )
            lines.append("")
        else:
            lines.append("No functions detected.\n")
    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <file_or_directory> [--format json|markdown]", file=sys.stderr)
        sys.exit(1)

    target = sys.argv[1]
    fmt = "json"
    if "--format" in sys.argv:
        idx = sys.argv.index("--format")
        if idx + 1 < len(sys.argv):
            fmt = sys.argv[idx + 1]

    reports = analyze_path(target)

    if fmt == "markdown":
        print(format_markdown(reports))
    else:
        print(json.dumps(reports, indent=2))
