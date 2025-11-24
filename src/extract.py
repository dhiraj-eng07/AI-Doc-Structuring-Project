import pdfplumber


def extract_text_from_pdf(path: str) -> str:
    """Extracts text from a text-based PDF and returns a single string."""
    text_parts = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    return "\n".join(text_parts)


if __name__ == '__main__':
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else '/mnt/data/Data Input.pdf'
    out = extract_text_from_pdf(path)
    print(out[:1000])
