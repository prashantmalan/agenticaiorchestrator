import requests
import xml.etree.ElementTree as ET
import logging

logger = logging.getLogger(__name__)

class FPMLDataTool:
    def __init__(self):
        self.data_registry = {}

    def fetch_and_parse_fpml(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            fpml_data = response.text

            # Parse the FPML XML
            root = ET.fromstring(fpml_data)
            trades = []
            for trade in root.findall('.//trade'):
                trade_data = {
                    "TradeDate": trade.findtext('tradeDate'),
                    "Counterparty": trade.findtext('.//partyReference'),
                    "Notional": trade.findtext('.//notionalAmount')
                }
                trades.append(trade_data)

            # Store in registry
            self.data_registry['trades'] = trades
            logger.info("FPML data fetched and parsed successfully")
        except Exception as e:
            logger.error(f"Error fetching or parsing FPML data: {str(e)}")
            raise

    def get_registry(self):
        return self.data_registry