#!/usr/bin/env python3
"""
Token Estimation for MCP-to-Skill Conversion

Estimates token costs for MCP tool schemas and compares with
the skill alternative. Uses character-based approximation
(~4 chars per token for English text, ~3.5 for JSON/code).

Usage:
    python3 estimate_tokens.py --mcp-tools <tool_count> --avg-schema-chars <chars>
    python3 estimate_tokens.py --schema-file <path_to_json>
    python3 estimate_tokens.py --raw-text <path_to_text_file>

Examples:
    python3 estimate_tokens.py --mcp-tools 15 --avg-schema-chars 800
    python3 estimate_tokens.py --schema-file tools_schema.json
    python3 estimate_tokens.py --raw-text tool_definitions.txt
"""

import sys
import json
import argparse
from pathlib import Path


# Approximation: ~3.5 characters per token for JSON/code content
CHARS_PER_TOKEN_CODE = 3.5
# Approximation: ~4 characters per token for English prose
CHARS_PER_TOKEN_PROSE = 4.0
# Skill metadata (name + description in system prompt) - typical range
SKILL_METADATA_TOKENS = (80, 200)
# Full SKILL.md loaded on trigger - typical range
SKILL_BODY_TOKENS = (500, 2000)


def estimate_tokens(char_count: int, content_type: str = "code") -> int:
    """Estimate token count from character count."""
    rate = CHARS_PER_TOKEN_CODE if content_type == "code" else CHARS_PER_TOKEN_PROSE
    return int(char_count / rate)


def estimate_from_tool_count(tool_count: int, avg_schema_chars: int = 800) -> dict:
    """Estimate from tool count and average schema size."""
    total_chars = tool_count * avg_schema_chars
    total_tokens = estimate_tokens(total_chars, "code")
    return {
        "tool_count": tool_count,
        "avg_schema_chars": avg_schema_chars,
        "total_schema_chars": total_chars,
        "estimated_tokens_per_turn": total_tokens,
    }


def estimate_from_file(file_path: str) -> dict:
    """Estimate from actual schema file content."""
    path = Path(file_path)
    content = path.read_text()
    char_count = len(content)

    if path.suffix == ".json":
        try:
            data = json.loads(content)
            if isinstance(data, list):
                tool_count = len(data)
            elif isinstance(data, dict) and "tools" in data:
                tool_count = len(data["tools"])
            else:
                tool_count = 1
        except json.JSONDecodeError:
            tool_count = "unknown"
        content_type = "code"
    else:
        tool_count = "unknown"
        content_type = "code"

    tokens = estimate_tokens(char_count, content_type)
    return {
        "tool_count": tool_count,
        "file_chars": char_count,
        "estimated_tokens_per_turn": tokens,
    }


def print_comparison(mcp_estimate: dict):
    """Print before/after comparison."""
    mcp_tokens = mcp_estimate["estimated_tokens_per_turn"]
    skill_meta_low, skill_meta_high = SKILL_METADATA_TOKENS
    skill_body_low, skill_body_high = SKILL_BODY_TOKENS

    print("\n" + "=" * 60)
    print("MCP-to-Skill Token Savings Estimate")
    print("=" * 60)

    print(f"\n📊 MCP Analysis:")
    print(f"   Tools:              {mcp_estimate.get('tool_count', 'unknown')}")
    print(f"   Schema size:        ~{mcp_estimate.get('total_schema_chars', mcp_estimate.get('file_chars', 0)):,} chars")
    print(f"   Tokens per turn:    ~{mcp_tokens:,}")

    print(f"\n📦 Skill Alternative:")
    print(f"   Metadata (always):  ~{skill_meta_low}-{skill_meta_high} tokens")
    print(f"   Body (when loaded): ~{skill_body_low}-{skill_body_high} tokens")

    # Savings calculation
    # Best case: skill not triggered at all (most turns)
    savings_best = mcp_tokens - skill_meta_high
    # Worst case: skill loaded every turn
    savings_worst = mcp_tokens - skill_meta_high - skill_body_high

    print(f"\n💰 Estimated Savings:")
    print(f"   Per turn (skill not loaded):  ~{savings_best:,} tokens ({savings_best/mcp_tokens*100:.0f}%)")
    print(f"   Per turn (skill loaded):      ~{max(0, savings_worst):,} tokens ({max(0, savings_worst)/mcp_tokens*100:.0f}%)")

    # Conversation-level estimate (assuming 20 turns, skill loaded 3 times)
    turns = 20
    skill_loaded_turns = 3
    conv_mcp = mcp_tokens * turns
    conv_skill = (skill_meta_high * turns) + (skill_body_high * skill_loaded_turns)
    conv_savings = conv_mcp - conv_skill

    print(f"\n📈 Over a {turns}-turn conversation (skill loaded ~{skill_loaded_turns} times):")
    print(f"   MCP total:          ~{conv_mcp:,} tokens")
    print(f"   Skill total:        ~{conv_skill:,} tokens")
    print(f"   Net savings:        ~{conv_savings:,} tokens ({conv_savings/conv_mcp*100:.0f}%)")

    if savings_best < 200:
        print(f"\n⚠️  Small MCP — conversion savings are marginal. Consider keeping as MCP.")
    elif savings_best > 2000:
        print(f"\n✅ High-value conversion — significant context savings.")
    else:
        print(f"\n👍 Moderate savings — conversion recommended if the tools are straightforward.")

    print()


def main():
    parser = argparse.ArgumentParser(description="Estimate MCP-to-Skill token savings")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--mcp-tools", type=int, help="Number of MCP tools")
    group.add_argument("--schema-file", type=str, help="Path to tool schema JSON/text file")
    group.add_argument("--raw-text", type=str, help="Path to raw tool definitions text file")

    parser.add_argument("--avg-schema-chars", type=int, default=800,
                       help="Average characters per tool schema (default: 800)")

    args = parser.parse_args()

    if args.mcp_tools:
        estimate = estimate_from_tool_count(args.mcp_tools, args.avg_schema_chars)
    elif args.schema_file:
        estimate = estimate_from_file(args.schema_file)
    elif args.raw_text:
        estimate = estimate_from_file(args.raw_text)

    print_comparison(estimate)


if __name__ == "__main__":
    main()
