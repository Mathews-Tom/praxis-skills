# Dependency Installation

## Prerequisites

- Python 3.10+. Verify: `python --version`
- `uv` package manager.

## Check Before Installing

```bash
uv pip show markitdown
```

Avoid redundant installs.

## Install Table

| Use case                    | Install command                                                        |
| --------------------------- | ---------------------------------------------------------------------- |
| Everything (recommended)    | `uv pip install 'markitdown[all]'`                                     |
| PDF only                    | `uv pip install 'markitdown[pdf]'`                                     |
| Office docs                 | `uv pip install 'markitdown[docx,pptx,xlsx]'`                          |
| Audio transcription         | `uv pip install 'markitdown[audio-transcription]'`                     |
| Azure Document Intelligence | `uv pip install 'markitdown[az-doc-intel]'`                            |
| URL fetching (static)       | `uv pip install trafilatura`                                           |
| URL fetching (JS-rendered)  | `uv pip install playwright && playwright install chromium`             |
| LLM image description       | `uv pip install anthropic`                                             |

## Recommended First Install

```bash
uv pip install 'markitdown[all]' trafilatura
```

This covers all file formats and static URL fetching. Add Playwright only if JS-rendered pages are needed.

## Verification

```bash
python -c "from markitdown import MarkItDown; print('markitdown OK')"
python -c "import trafilatura; print('trafilatura OK')"
```
