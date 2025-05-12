import os
import zipfile
from PyPDF2 import PdfReader
import requests
from crew import ComplianceCrew
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ComplianceSystem:
    def __init__(self):
        self.crew = ComplianceCrew()

    def extract_zip(self, zip_path, extract_to):
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
            logger.info(f"Successfully extracted ZIP file to {extract_to}")
        except Exception as e:
            logger.error(f"Error extracting ZIP file: {str(e)}")
            raise

    def read_regulatory_docs(self, directory):
        try:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if file.endswith('.pdf'):
                        file_path = os.path.join(root, file)
                        logger.info(f"Processing PDF: {file_path}")
                        with open(file_path, 'rb') as f:
                            reader = PdfReader(f)
                            for page in reader.pages:
                                text = page.extract_text()
                                if text:
                                    logger.info(f"Extracted text preview: {text[:100]}")
        except Exception as e:
            logger.error(f"Error reading regulatory documents: {str(e)}")
            raise

    def fetch_trade_data(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            logger.info("Successfully fetched trade data")
            return response.content
        except Exception as e:
            logger.error(f"Error fetching trade data: {str(e)}")
            raise

    def run(self):
        try:
            # Configuration
            local_zip_path = r"C:\Users\user\Downloads\AIDG_v2_0.zip"
            extract_directory = r"C:\Users\user\Downloads\AIDG"
            trade_data_url = "https://www.fpml.org/spec/fpml-5-3-6-rec-1/html/confirmation/xml/products/interest-rate-derivatives/ird-ex01-vanilla-swap.xml"

            # Extract and process documents
            self.extract_zip(local_zip_path, extract_directory)
            self.read_regulatory_docs(extract_directory)
            trade_data = self.fetch_trade_data(trade_data_url)

            # Run the workflow
            result = self.crew.run_workflow()
            logger.info(f"Workflow result: {result}")

        except Exception as e:
            logger.error(f"Error in main execution: {str(e)}")
            raise

if __name__ == "__main__":
    system = ComplianceSystem()
    system.run()