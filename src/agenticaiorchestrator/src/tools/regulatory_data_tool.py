import os
from PyPDF2 import PdfReader
import logging
from langchain.tools import tool

logger = logging.getLogger(__name__)

class RegulatoryTools:

    @tool("Process regulatory PDF documents")
    def read_regulatory_docs(directory: str) -> str:
        """Reads and processes PDF files from a specified directory, extracting text for each document."""
        try:
            data_registry = {}
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
                            data_registry[file_name] = text
                            logger.debug(f"Stored text for {file_name}")
            return "Regulatory documents processed successfully."
        except Exception as e:
            logger.error(f"Error reading regulatory documents: {str(e)}")
            return "Failed to process regulatory documents."

# Example usage:
# result = RegulatoryTools.read_regulatory_docs(directory='path/to/regulatory/docs')
# print(result)