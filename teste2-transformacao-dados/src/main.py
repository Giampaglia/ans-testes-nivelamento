import os
from extractor import extract_data_from_pdf
from processor import replace_abbreviations
from saver import save_to_csv
from compressor import compress_file

def main():
    # Caminho para o PDF (Anexo I)
    pdf_path = "path_to_your_pdf_file.pdf"
    
    # Extração de dados
    extracted_data = extract_data_from_pdf(pdf_path)
    
    # Processamento dos dados (substituindo abreviações)
    processed_data = replace_abbreviations(extracted_data)
    
    # Caminho para o CSV
    csv_path = "output_data.csv"
    
    # Salvando os dados no CSV
    save_to_csv(processed_data, csv_path)
    
    # Caminho para o arquivo ZIP
    zip_path = "Teste_nome_do_usuario.zip"
    
    # Compactando o CSV em ZIP
    compress_file(csv_path, zip_path)

    print("✅ Processo concluído com sucesso!")

if __name__ == "__main__":
    main()
