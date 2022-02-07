# PDF-extractor
Extracts text from pdf by converting them to images and using tesseract-ocr.

---

## requirements
bs4, lxml, pdf2image, pytesseract, requests

---
Before using pytesseract we need to download tesseract.exe and configure it as 

```python

import pytesseract
pytesseract.pytesseract.tesseract_cmd="<path-to-exe-file>"

```

Also, for pdf2image we need to download and configure poppler bin directory as

```python


from pdf2image import convert_from_path
pages = convert_from_path(<pdf-path>, dpi, poppler_path="path-to-poppler-bin-directory")


```
