import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging
from typing import List, Optional

class ANSScraper:
    """Classe para scraping de documentos PDF de sites governamentais."""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self._setup_logging()
        self._setup_session()

    def _setup_logging(self):
        """Configura sistema de logs."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('scraper.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def _setup_session(self):
        """Configura headers da sessão HTTP."""
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Language': 'pt-BR,pt;q=0.9'
        })

    def find_pdf_links(self) -> List[str]:
        """Encontra links de PDFs nos Anexos I e II."""
        try:
            soup = BeautifulSoup(self.session.get(self.base_url).content, 'html.parser')
            return [
                urljoin(self.base_url, a['href'])
                for a in soup.select('a[href$=".pdf"]')
                if any(keyword in a.get('href', '').lower() 
                      for keyword in ['anexo-i', 'anexo_ii'])
            ]
        except Exception as e:
            self.logger.error(f"Erro ao buscar links: {str(e)}")
            return []

    def download_pdfs(self, pdf_urls: List[str], output_dir: str = 'downloads') -> List[str]:
        """Baixa PDFs e retorna lista de caminhos locais."""
        os.makedirs(output_dir, exist_ok=True)
        saved_files = []
        
        for url in pdf_urls:
            try:
                filename = os.path.join(output_dir, os.path.basename(url))
                with open(filename, 'wb') as f:
                    f.write(self.session.get(url).content)
                saved_files.append(filename)
            except Exception as e:
                self.logger.error(f"Falha ao baixar {url}: {str(e)}")
        return saved_files