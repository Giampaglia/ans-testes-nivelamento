from scraper import PDFScraper

def main():
    URL_ANS = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
    OUTPUT_DIR = "downloads"
    
    scraper = PDFScraper(URL_ANS)
    
    # Corrigindo o nome da variável para attachments (ou o nome que você está usando)
    attachments = scraper.find_attachments()  # Ou find_pdf_links() dependendo do seu método
    
    if attachments:  # Verifica se encontrou os anexos
        # Corrigindo a chamada do método download_pdfs
        downloaded_files = scraper.download_pdfs(attachments, OUTPUT_DIR)
        
        if downloaded_files:
            print("✅ Downloads concluídos com sucesso!")
            print(f"Arquivos salvos em: {OUTPUT_DIR}")
        else:
            print("❌ Falha ao baixar os arquivos")
    else:
        print("⚠️ Nenhum anexo encontrado")

if __name__ == "__main__":
    main()