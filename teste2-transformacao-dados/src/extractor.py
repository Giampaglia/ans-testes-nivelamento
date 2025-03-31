import fitz  # PyMuPDF

def extract_data_from_pdf(pdf_path: str):
    """Extraí os dados do PDF do Anexo I."""
    doc = fitz.open(pdf_path)
    data = []

    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text = page.get_text("text")
        
        # Aqui você faria a extração de dados específica da tabela
        # Exemplo de extração, ajustado conforme necessário:
        lines = text.split("\n")
        for line in lines:
            data.append(line.split())

    return data
