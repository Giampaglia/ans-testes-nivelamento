import zipfile
import os

def compress_file(file_path, zip_path):
    """Compacta o arquivo CSV em um arquivo ZIP."""
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(file_path, os.path.basename(file_path))
