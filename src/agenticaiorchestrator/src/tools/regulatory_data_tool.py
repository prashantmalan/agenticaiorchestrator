import os
from PyPDF2 import PdfReader
import logging

logger = logging.getLogger(__name__)

class RegulatoryDataTool:
    def __init__(self):
        self.data_registry = {}

    def read_regulatory_docs(self, directory):
        try:
            for root, dirs, files in os.walk(directory):
                for file_name in files:
                    if file_name.endswith('.pdf'):
                        file_path = os.path.join(root, file_name)
                        logger.info(f"Processing PDF: {file_path}")
                        with open(file_path, 'rb') as f:
                            reader = PdfReader(f)
                            text = ""
                            for page in reader.pages:
                                page_text = page.extract_text()
                                if page_text:
                                    text += page_text
                            self.data_registry[file_name] = text
                            logger.debug(f"Stored text for {file_name}")
        except Exception as e:
            logger.error(f"Error reading regulatory documents: {str(e)}")
            raise

    def get_registry(self):
        return self.data_registry