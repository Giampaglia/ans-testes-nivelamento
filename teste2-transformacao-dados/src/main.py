import fitz  # PyMuPDF
import csv
import os
import re
import zipfile

def extract_tables_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    data = []

    # Cabeçalhos com os nomes completos conforme exigido
    headers = [
        "PROCEDIMENTO", 
        "RN (alteração)", 
        "VIGÊNCIA", 
        "OD: Seg. Odontológica",  # Nome completo
        "AMB: Seg. Ambulatorial",  # Nome completo
        "HCO: Seg. Hospitalar Com Obstetrícia",  # Sugestão para manter padrão
        "HSO: Seg. Hospitalar Sem Obstetrícia",  # Sugestão para manter padrão
        "REF: Plano Referência",  # Sugestão para manter padrão
        "PAC: Procedimento de Alta Complexidade",  # Sugestão para manter padrão
        "DUT: Diretriz de Utilização",  # Sugestão para manter padrão
        "SUBGRUPO", 
        "GRUPO", 
        "CAPÍTULO"
    ]
    
    # Extrai os dados do PDF
    for page in doc:
        text = page.get_text()
        for line in text.split('\n'):
            if re.match(r'^[A-Z0-9].*', line):  # Filtra linhas que começam com letras ou números
                columns = re.split(r'\s{2,}', line.strip())  # Divide por 2 ou mais espaços
                if len(columns) > 0:
                    row = columns + [''] * (len(headers) - len(columns))  # Preenche colunas faltantes
                    data.append(row)
    
    return [headers] + data

def clean_text(text):
    # Corrige caracteres comuns em PDFs
    replacements = {
        "�": "í", 
        "SA�DE": "SAÚDE", 
        "�NICO": "ÚNICO"
    }
    for wrong, right in replacements.items():
        text = text.replace(wrong, right)
    return text

def replace_abbreviations(data):
    # Substitui as abreviações por suas descrições completas
    for row in data:
        for i, value in enumerate(row):
            if value == "OD":
                row[i] = "Seg. Odontológica"
            elif value == "AMB":
                row[i] = "Seg. Ambulatorial"
    return data

def save_to_csv(data, csv_path):
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerows(data)

def compress_to_zip(csv_path, zip_path):
    # Compacta o arquivo CSV em um arquivo ZIP
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(csv_path, os.path.basename(csv_path))

def main():
    print("Iniciando processamento...")
    pdf_path = r"C:\Users\leona\OneDrive\Documentos\GitHub\ans-testes-nivelamento\teste1-web-scraping\src\downloads\Anexo_I.pdf"  # Caminho do PDF
    csv_path = r"C:\Users\leona\OneDrive\Documentos\GitHub\ans-testes-nivelamento\teste2-transformacao-dados\src\output\output.csv"  # Caminho do CSV
    zip_path = r"C:\Users\leona\OneDrive\Documentos\GitHub\ans-testes-nivelamento\teste2-transformacao-dados\src\output\Teste_Leonardo_Giampaglia_Gomes.zip"  # Caminho do arquivo ZIP
    
    # Extrair dados do PDF
    data = extract_tables_from_pdf(pdf_path)
    
    # Limpar e substituir abreviações
    cleaned_data = [[clean_text(cell) for cell in row] for row in data]
    cleaned_data = replace_abbreviations(cleaned_data)
    
    # Salvar dados no CSV
    save_to_csv(cleaned_data, csv_path)
    print(f"Dados salvos em: {csv_path}")
    
    # Compactar o CSV em um arquivo ZIP
    compress_to_zip(csv_path, zip_path)
    print(f"Arquivo compactado em: {zip_path}")

# Esta parte deve estar no final do arquivo e sem indentação
if __name__ == "__main__":
    main()
