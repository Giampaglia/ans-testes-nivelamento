import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import zipfile
import logging
from typing import List, Optional

class ANSScraper:
    """
    Classe para scraping do site da ANS e download de Anexos I e II em PDF.
    """
    
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
        """
        Encontra links para os Anexos I e II no site da ANS.
        
        Returns:
            List[str]: URLs dos PDFs encontrados
        """
        try:
            soup = self._get_page_content(self.base_url)
            if not soup:
                return []

            pdf_links = []
            for link in soup.find_all('a', href=True):
                text = link.get_text().strip().lower()
                if any(keyword in text for keyword in ['anexo i', 'anexo ii']):
                    pdf_url = urljoin(self.base_url, link['href'])
                    if pdf_url.lower().endswith('.pdf'):
                        pdf_links.append(pdf_url)
                        self.logger.info(f"Link encontrado: {pdf_url}")
            
            return pdf_links

        except Exception as e:
            self.logger.error(f"Erro ao buscar links: {str(e)}")
            return []

    # ... (continua com os outros métodos)