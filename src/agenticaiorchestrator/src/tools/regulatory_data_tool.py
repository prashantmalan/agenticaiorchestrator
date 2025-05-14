import os
import zipfile
from PyPDF2 import PdfReader
import logging
from langchain.tools import tool

logger = logging.getLogger(__name__)

class RegulatoryTools:
    def __init__(self):
        pass

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

    def read(self, zip_file_path):
        """
        Reads and processes regulatory data from the given ZIP file.

        Args:
            zip_file_path (str): The path to the ZIP file containing regulatory documents.

        Returns:
            list: A list of file names extracted from the ZIP file.
        """
        try:
            if not os.path.exists(zip_file_path):
                raise FileNotFoundError(f"File not found: {zip_file_path}")

            # Extract the ZIP file
            extracted_files = []
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                extract_path = os.path.join(os.path.dirname(zip_file_path), "extracted_regulatory_docs")
                zip_ref.extractall(extract_path)
                extracted_files = zip_ref.namelist()

            print(f"Extracted files: {extracted_files}")
            return extracted_files
        except FileNotFoundError as e:
            print(f"Error: {e}")
            return None
        except zipfile.BadZipFile as e:
            print(f"Error: Invalid ZIP file: {e}")
            return None

# Example usage:
# result = RegulatoryTools.read_regulatory_docs(directory='path/to/regulatory/docs')
# print(result)