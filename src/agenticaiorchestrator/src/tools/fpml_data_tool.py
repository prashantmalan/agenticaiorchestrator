import requests
from xml.etree import ElementTree
import pandas as pd
import logging
import os
from langchain.tools import tool

logger = logging.getLogger(__name__)

class FPMLDataTools:
    def __init__(self):
        pass

    @tool("Fetch and parse FPML data")
    def fetch_and_parse_fpml(url: str) -> str:
        """Fetches FPML data from a URL, parses it, and saves it to a CSV file."""
        try:
            # Fetch the FpML data from the URL
            response = requests.get(url)
            print(f"Fetching data from {url}")
            if response.status_code != 200:
                raise requests.exceptions.RequestException(f"Failed to fetch data: {response.status_code}")
            response.raise_for_status()  # Raise an error for HTTP issues

            # Parse the XML content
            xml_content = ElementTree.fromstring(response.content)
            elements = []

            # Recursively parse the XML tree
            FPMLDataTools._parse_element(xml_content, [], elements)

            # Save to CSV
            FPMLDataTools.save_to_csv(elements)

            return "FPML data fetched, parsed, and saved to CSV successfully."
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching FPML data: {e}")
            return "Failed to fetch FPML data."
        except ElementTree.ParseError as e:
            logger.error(f"Error parsing FPML XML: {e}")
            return "Failed to parse FPML data."

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

    def read(self, url):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(url, headers=headers, timeout=10, verify=False)
            logger.info(f"Response Status Code: {response.status_code}")
            logger.info(f"Response Content: {response.text[:500]}")  # Log first 500 characters
            response.raise_for_status()
            xml_content = ElementTree.fromstring(response.content)
            return self._parse_fpml(xml_content)
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching FpML data: {e}")
            return None
        except ElementTree.ParseError as e:
            logger.error(f"Error parsing FpML XML: {e}")
            return None

    def _parse_fpml(self, xml_content):
        """
        Parses the FpML XML content into a structured format.

        Args:
            xml_content (ElementTree.Element): The root of the FpML XML tree.

        Returns:
            dict: Parsed FpML data.
        """
        # Example: Extracting some basic information from the XML
        parsed_data = {}
        for child in xml_content:
            parsed_data[child.tag] = child.text
        return parsed_data

# Example usage:
# result = FPMLTools.fetch_and_parse_fpml(url='http://example.com/fpml.xml')
# print(result)