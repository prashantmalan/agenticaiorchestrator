import requests
import xml.etree.ElementTree as ET
import pandas as pd
import logging
import os
from langchain.tools import tool

logger = logging.getLogger(__name__)

class FPMLDataTools:

    @tool("Fetch and parse FPML data")
    def fetch_and_parse_fpml(url: str) -> str:
        """Fetches FPML data from a URL, parses it, and saves it to a CSV file."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            fpml_data = response.text

            # Parse the FPML XML
            root = ET.fromstring(fpml_data)
            elements = []

            # Recursively parse the XML tree
            FPMLDataTools._parse_element(root, [], elements)

            # Save to CSV
            FPMLDataTools.save_to_csv(elements)

            return "FPML data fetched, parsed, and saved to CSV successfully."
        except Exception as e:
            logger.error(f"Error fetching or parsing FPML data: {str(e)}")
            return "Failed to process FPML data."

    @staticmethod
    def _parse_element(element, path, elements):
        current_path = path + [element.tag]

        # Store element's value and attributes
        data_entry = {
            'xpath': '/'.join(current_path),
            'value': element.text.strip() if element.text else None,
            'attributes': {k: v for k, v in element.attrib.items()}
        }
        elements.append(data_entry)

        # Recurse into child elements
        for child in element:
            FPMLDataTools._parse_element(child, current_path, elements)

    @staticmethod
    def save_to_csv(elements):
        # Convert data to a DataFrame
        df = pd.DataFrame(elements)

        # Define CSV file path
        csv_path = r"C:\Users\user\agenticaiorchestrator\data\fpml_data.csv"

        # Ensure the directory exists
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)

        # Save DataFrame to CSV
        df.to_csv(csv_path, index=False)
        logger.info(f"Data saved to CSV at {csv_path}")

# Example usage:
# result = FPMLTools.fetch_and_parse_fpml(url='http://example.com/fpml.xml')
# print(result)