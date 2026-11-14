import fitz

def extract_text(pdf_path):
    document = fitz.open(pdf_path)

    pages_data = []

    for page_number, page in enumerate(document, start=1):

        page_text = page.get_text()

        pages_data.append({
            "page_number": page_number,
            "text": page_text
        })

    document.close()

    return pages_data