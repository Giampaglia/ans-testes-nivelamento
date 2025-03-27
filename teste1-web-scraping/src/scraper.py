import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging
from typing import List, Optional, Dict, Set

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
            handlers=[
                logging.FileHandler('scraper.log'),
                logging.StreamHandler()
            ]
        )
    
    def _get_page_content(self) -> Optional[BeautifulSoup]:
        """Obtém e parseia o conteúdo HTML da página."""
        try:
            response = self.session.get(self.base_url, timeout=15)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            self.logger.error(f"Falha ao acessar {self.base_url}: {str(e)}")
            return None
    
    def _identify_attachment(self, url: str) -> Optional[str]:
        """Identifica se a URL pertence a Anexo I ou II."""
        patterns: Dict[str, List[str]] = {
            'Anexo I': ['anexo-i', 'anexo_i', 'anexo1', 'anexo i'],
            'Anexo II': ['anexo-ii', 'anexo_ii', 'anexo2', 'anexo ii']
        }
        
        url_lower = url.lower()
        for attachment, patterns_list in patterns.items():
            if any(pattern in url_lower for pattern in patterns_list):
                return attachment
        return None
    
    def find_attachments(self) -> Dict[str, str]:
        """
        Busca e retorna os links dos Anexos I e II em ordem prioritária.
        
        Returns:
            Dict[str, str]: Dicionário com chaves 'Anexo I' e 'Anexo II' e URLs como valores
        """
        try:
            soup = self._get_page_content()
            if not soup:
                self.logger.warning("Não foi possível obter o conteúdo da página")
                return {}

            attachments = {}
            patterns = {
                'Anexo I': [
                    'anexoi', 'anexo-i', 'anexo_i', 
                    'anexo1', 'anexo 1', 'i_rol',
                    'i-rnl', 'rol_i', 'anexoi_'
                ],
                'Anexo II': [
                    'anexoii', 'anexo-ii', 'anexo_ii',
                    'anexo2', 'anexo 2', 'ii_rol',
                    'ii-rnl', 'rol_ii', 'anexoii_'
                ]
            }

            # Primeira passada: busca prioritária pelo Anexo I
            for link in soup.select('a[href*=".pdf"], a[href*=".PDF"]'):
                href = link['href'].lower()
                if any(p in href for p in patterns['Anexo I']):
                    attachments['Anexo I'] = urljoin(self.base_url, link['href'])
                    self.logger.info(f"Anexo I encontrado: {attachments['Anexo I']}")
                    break

            # Segunda passada: busca pelo Anexo II apenas se o I foi encontrado
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

    def download_pdfs(self, attachments: Dict[str, str], output_dir: str = 'downloads') -> Dict[str, str]:
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

    def run(self, output_dir: str = 'downloads') -> Dict[str, str]:
        """Executa o fluxo completo de scraping e download."""
        attachments = self.find_attachments()
        if not attachments:
            self.logger.warning("Nenhum anexo encontrado")
            return {}
            
        return self.download_pdfs(attachments, output_dir)