from scraper import ANSScraper

def main():
    URL_ANS = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
    
    scraper = ANSScraper(URL_ANS)
    
    # Etapa 1: Buscar links dos PDFs
    pdf_links = scraper.find_pdf_links()
    if not pdf_links:
        print("❌ Nenhum PDF encontrado!")
        return

    # Etapa 2: Download dos arquivos
    downloaded_files = scraper.download_pdfs(pdf_links)
    
    # Etapa 3: Compactação
    if downloaded_files:
        scraper.create_zip(downloaded_files)
        print("✅ Processo concluído com sucesso!")
    else:
        print("❌ Falha ao baixar arquivos.")

if __name__ == "__main__":
    main()