# md-to-pdf

A Claude skill that converts Markdown files to professionally styled PDF documents with full support for **Mermaid diagrams**, **LaTeX math (KaTeX)**, **tables**, **syntax-highlighted code blocks**, and all standard Markdown features.

## Quick Start

```bash
# 1. Check dependencies
bash scripts/setup.sh

# 2. Convert
python3 scripts/md_to_pdf.py input.md output.pdf

# 3. With options
python3 scripts/md_to_pdf.py input.md output.pdf --format Letter --header-footer --landscape
```

## Installation as a Claude Skill

Copy the `md-to-pdf/` directory into your agent's skills folder:

```text
<skills-dir>/md-to-pdf/
├── SKILL.md
├── LICENSE.txt
├── README.md
├── scripts/
│   ├── md_to_pdf.py
│   ├── katex_render.js
│   └── setup.sh
└── tests/
    └── test_document.md
```

The skill auto-triggers when Claude sees requests like "convert this markdown to PDF" or "export as PDF".

## Rendering Pipeline

```text
Markdown → [mmdc: Mermaid→SVG] → [pandoc: MD→HTML] → [KaTeX: LaTeX→HTML] → [Playwright: HTML→PDF]
```

Each stage is independently skippable (`--no-mermaid`, `--no-math`) for speed when features aren't needed.

## Dependencies

| Tool       | Purpose       | Install                                                 |
| ---------- | ------------- | ------------------------------------------------------- |
| pandoc     | MD → HTML     | `apt install pandoc`                                    |
| mmdc       | Mermaid → SVG | `npm install -g @mermaid-js/mermaid-cli`                |
| katex      | LaTeX → HTML  | `npm install -g katex`                                  |
| playwright | HTML → PDF    | `pip install playwright && playwright install chromium` |

All are pre-installed in the standard Claude computer-use environment. Run `bash scripts/setup.sh` to verify.

## Options

| Flag              | Default | Description                             |
| ----------------- | ------- | --------------------------------------- |
| `--format`        | A4      | A4 / Letter / Legal / A3                |
| `--margin`        | 0.75in  | Single value or `top,right,bottom,left` |
| `--landscape`     | off     | Landscape orientation                   |
| `--header-footer` | off     | Page numbers in footer                  |
| `--css`           | none    | Custom CSS file to layer on top         |
| `--no-mermaid`    | off     | Skip Mermaid rendering                  |
| `--no-math`       | off     | Skip KaTeX rendering                    |

## Customization

**Custom CSS**: `--css custom.css` injects after defaults (your rules win).

**Mermaid theming**: `MERMAID_CONFIG=/path/to/.mermaidrc python3 scripts/md_to_pdf.py ...`

## Testing

```bash
python3 scripts/md_to_pdf.py tests/test_document.md test_output.pdf --header-footer
```

The test document exercises all supported features: 4 Mermaid diagram types, inline + display math, tables, code blocks in 3 languages, footnotes, definition lists, blockquotes, and text formatting.

## License

MIT — see [LICENSE.txt](LICENSE.txt).
