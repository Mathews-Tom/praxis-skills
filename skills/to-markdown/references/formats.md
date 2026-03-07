# Format-Specific Handling

Per-format conversion details, internal engines, known issues, and workarounds.

## Format Table

| Format          | Engine (internal)       | Known Issues                                      | Workaround                                      |
| --------------- | ----------------------- | ------------------------------------------------- | ----------------------------------------------- |
| PDF (text)      | pdfminer                | Multi-column layouts merge columns                | Acceptable for LLM use                          |
| PDF (scanned)   | pdfminer                | Returns empty — no text layer                     | OCR: Azure DocIntel or Tesseract (see below)    |
| DOCX            | python-docx             | Embedded images lost                              | Use LLM client for image descriptions           |
| PPTX            | python-pptx             | Speaker notes included (useful for LLMs)          | Filter with `---NOTES---` marker if needed      |
| XLSX / XLS      | openpyxl / xlrd         | Each sheet becomes a Markdown table               | Works well                                      |
| HTML            | html2text               | Complex layouts lose structure                    | Use Turndown for fidelity-critical cases        |
| Images          | EXIF + optional OCR     | No OCR without Azure DocIntel                     | Pass `docintel_endpoint` for OCR                |
| Audio           | speech transcription    | Requires `[audio-transcription]` extra            | `uv pip install 'markitdown[audio-transcription]'` |
| YouTube         | transcript API          | Only works if captions available                  | Returns empty if no captions                    |
| CSV / JSON / XML | built-in               | Converts to Markdown tables/structure             | Clean, reliable                                 |
| EPub            | built-in                | Large EPubs may be slow                           | Works for most cases                            |

## Scanned PDF — OCR Escalation Path

When markitdown returns empty or near-empty output from a PDF, the file is likely scanned (image-only, no text layer).

### Option 1: Azure Document Intelligence

```python
from markitdown import MarkItDown

md = MarkItDown(docintel_endpoint="https://<resource>.cognitiveservices.azure.com/")
result = md.convert("scanned.pdf")
```

Requires an Azure AI Document Intelligence resource. Set the endpoint and key via environment variables or pass directly.

### Option 2: Tesseract (local OCR)

```bash
# Install Tesseract
brew install tesseract  # macOS
# apt install tesseract-ocr  # Linux

# Extract images from PDF, then OCR
uv pip install pdf2image pytesseract
```

```python
from pdf2image import convert_from_path
import pytesseract

images = convert_from_path("scanned.pdf")
text = "\n\n".join(pytesseract.image_to_string(img) for img in images)
```

This is a fallback outside markitdown's pipeline. Use when Azure DocIntel is unavailable.

## PPTX Speaker Notes

Markitdown includes speaker notes by default, separated by `---NOTES---` markers. For LLM ingestion this is typically desirable. To strip notes:

```python
import re

cleaned = re.sub(r"---NOTES---.*?(?=^#|\Z)", "", result.text_content, flags=re.DOTALL | re.MULTILINE)
```

## DOCX with Embedded Images

Images in DOCX files are not extracted by default. To get image descriptions, enable the LLM client (see SKILL.md "LLM Image Description" section). Without it, images are silently skipped.

## HTML Fidelity

markitdown uses `html2text` which handles standard article content well but loses structure on:
- Nested tables (common in email templates)
- CSS-dependent layouts (grid, flexbox)
- Interactive elements (forms, JS-rendered content)

For high-fidelity HTML-to-Markdown conversion where DOM structure matters, use Turndown via Node subprocess:

```bash
npx turndown-cli input.html -o output.md
```

This is out of scope for this skill — mention it as an alternative when html2text output is insufficient.
