import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging
import zipfile

class PDFScraper:
    """Classe otimizada para scraping de documentos PDF com tratamento robusto de erros."""
    
    def __init__(self, base_url: str):
        """Inicializa o scraper com configurações padrão."""
        self.base_url = base_url
        self.session = self._create_session()
        self._configure_logging()
        self.logger = logging.getLogger(__name__)
        
    def _create_session(self) -> requests.Session:
        """Cria e configura a sessão HTTP."""
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Language': 'pt-BR,pt;q=0.9',
            'Accept': 'application/pdf, text/html'
        })
        return session
    
    def _configure_logging(self):
        """Configura o sistema de logging."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[logging.FileHandler('scraper.log'), logging.StreamHandler()]
        )
    
    def _get_page_content(self) -> BeautifulSoup:
        """Obtém e parseia o conteúdo HTML da página."""
        try:
            response = self.session.get(self.base_url, timeout=15)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            self.logger.error(f"Falha ao acessar {self.base_url}: {str(e)}")
            return None
    
    def find_attachments(self) -> dict:
        """Busca e retorna os links dos Anexos I e II em ordem prioritária."""
        try:
            soup = self._get_page_content()
            if not soup:
                self.logger.warning("Não foi possível obter o conteúdo da página")
                return {}

            attachments = {}
            patterns = {
                'Anexo I': ['anexo-i', 'anexo_i', 'anexo1', 'anexo 1'],
                'Anexo II': ['anexo-ii', 'anexo_ii', 'anexo2', 'anexo 2']
            }

            for link in soup.select('a[href*=".pdf"], a[href*=".PDF"]'):
                href = link['href'].lower()
                if any(p in href for p in patterns['Anexo I']):
                    attachments['Anexo I'] = urljoin(self.base_url, link['href'])
                    self.logger.info(f"Anexo I encontrado: {attachments['Anexo I']}")
                    break

            if 'Anexo I' in attachments:
                for link in soup.select('a[href*=".pdf"], a[href*=".PDF"]'):
                    href = link['href'].lower()
                    if any(p in href for p in patterns['Anexo II']):
                        attachments['Anexo II'] = urljoin(self.base_url, link['href'])
                        self.logger.info(f"Anexo II encontrado: {attachments['Anexo II']}")
                        break

            return attachments

        except Exception as e:
            self.logger.error(f"Erro ao buscar anexos: {str(e)}")
            return {}

    def download_pdfs(self, attachments: dict, output_dir: str = 'downloads') -> dict:
        """Baixa os PDFs e retorna os caminhos locais."""
        os.makedirs(output_dir, exist_ok=True)
        local_files = {}
        
        for attachment_type, url in attachments.items():
            try:
                filename = os.path.join(output_dir, f"{attachment_type.replace(' ', '_')}.pdf")
                
                with self.session.get(url, stream=True, timeout=30) as response:
                    response.raise_for_status()
                    with open(filename, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                
                local_files[attachment_type] = filename
                self.logger.info(f"Download concluído: {filename}")
                
            except requests.RequestException as e:
                self.logger.error(f"Falha ao baixar {attachment_type}: {str(e)}")
        
        return local_files

    def compactar_anexos(self, output_dir: str = 'downloads', zip_name: str = 'Anexos_Compactados.zip') -> bool:
        """
        Compacta todos os arquivos PDF encontrados no diretório de saída em um único arquivo ZIP.
        
        Args:
            output_dir: Diretório onde os arquivos PDF estão localizados.
            zip_name: Nome do arquivo ZIP a ser criado.
            
        Returns:
            bool: True se a compactação foi bem-sucedida, False caso contrário.
        """
        # Lista todos os arquivos PDF no diretório de saída
        arquivos_pdf = [arq for arq in os.listdir(output_dir) if arq.lower().endswith('.pdf')]
        
        if not arquivos_pdf:
            self.logger.error("Nenhum arquivo PDF encontrado para compactar")
            return False
        
        try:
            # Caminho completo do arquivo ZIP
            zip_path = os.path.join(output_dir, zip_name)
            
            # Cria o arquivo ZIP
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for arquivo in arquivos_pdf:
                    # Adiciona o arquivo ao ZIP mantendo apenas o nome do arquivo (sem o caminho completo)
                    zipf.write(os.path.join(output_dir, arquivo), arquivo)
                    self.logger.info(f"Adicionado: {arquivo} ao ZIP")
            
            self.logger.info(f"Compactação concluída com sucesso: {zip_path}")
            return True
        
        except Exception as e:
            self.logger.error(f"Erro inesperado ao compactar: {str(e)}")
            return False


def main():
    URL_ANS = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
    OUTPUT_DIR = "downloads"
    
    scraper = PDFScraper(URL_ANS)
    
    # Encontre os anexos
    attachments = scraper.find_attachments()
    
    if attachments:  # Verifica se encontrou os anexos
        # Faz o download dos arquivos
        downloaded_files = scraper.download_pdfs(attachments, OUTPUT_DIR)
        
        if downloaded_files:
            print("✅ Downloads concluídos com sucesso!")
            print(f"Arquivos salvos em: {OUTPUT_DIR}")
            
            # Compacta os arquivos baixados em um único ZIP
            if scraper.compactar_anexos(OUTPUT_DIR):
                print("✅ Compactação concluída com sucesso!")
            else:
                print("❌ Falha na compactação dos arquivos.")
                
        else:
            print("❌ Falha ao baixar os arquivos")
    else:
        print("⚠️ Nenhum anexo encontrado")


if __name__ == "__main__":
    main()
