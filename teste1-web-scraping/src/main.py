from scraper import ANSScraper

def main():
    # Configuração
    URL_ANS = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
    OUTPUT_DIR = "anexos_baixados"
    
    # Processamento
    scraper = ANSScraper(URL_ANS)
    
    if (pdf_links := scraper.find_pdf_links()):
        if (downloaded_files := scraper.download_pdfs(pdf_links, OUTPUT_DIR)):
            print(f"✅ Downloads concluídos em: {OUTPUT_DIR}")
        else:
            print("❌ Falha nos downloads")
    else:
        print("⚠️ Nenhum PDF encontrado")

if __name__ == "__main__":
    main()