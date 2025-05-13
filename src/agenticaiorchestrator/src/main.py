import os
import zipfile
import logging
from crew import ComplianceCrew
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
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
            with open("extraction_log.txt", "w") as file:
                file.write(f"Extracted files to {extract_to}\n")
        except Exception as e:
            logger.error(f"Error extracting ZIP file: {str(e)}")
            raise

    def run(self):
        try:
            # Configuration
            local_zip_path = r"C:\Users\user\Downloads\AIDG_v2_0.zip"
            extract_directory = r"C:\Users\user\Downloads\AIDG"
            trade_data_url = "https://www.fpml.org/spec/fpml-5-3-6-rec-1/html/confirmation/xml/products/interest-rate-derivatives/ird-ex01-vanilla-swap.xml"

            # Extract documents
            self.extract_zip(local_zip_path, extract_directory)

            # Use the ComplianceCrew tools
            self.crew.regulatory_tool.read_regulatory_docs(extract_directory)
            self.crew.fpml_tool.fetch_and_parse_fpml(trade_data_url)  # Pass the correct URL variable

            # Run the workflow
            result = self.crew.run_workflow()
            logger.info(f"Workflow result: {result}")

            with open("workflow_result.txt", "w") as file:
                file.write(f"Workflow result: {result}\n")

        except Exception as e:
            logger.error(f"Error in main execution: {str(e)}")
            raise

if __name__ == "__main__":
    load_dotenv()  # Ensure environment variables are loaded
    system = ComplianceSystem()
    system.run()