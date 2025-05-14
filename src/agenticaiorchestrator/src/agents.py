from crewai import Agent
from textwrap import dedent
from tools.fpml_data_tool import FPMLDataTools
from tools.regulatory_data_tool import RegulatoryTools
from crewai_tools import XMLSearchTool

class RegulatoryAgents:
    def __init__(self,llm):
        self.fpml_tool = FPMLDataTools()
        self.regulatory_tool = RegulatoryTools()
        self.llm=llm
    def trade_data_ingestion_agent(self):
        return Agent(
            role="Data Ingestion",
            backstory="Responsible for ingesting data and preparing it for mapping.",
            goal="Read FPML data and generate a CSV with column names and values.",
            #tools=[self.fpml_tool.fetch_and_parse_fpml],
            tools=[
                XMLSearchTool(
                    xml_folder=r"C:\Users\user\agenticaiorchestrator\data\fpml"  # Specify the folder containing XML files
            )
            ],
            verbose=True,
        )

    def regulatory_data_ingestion_agent(self):
        return Agent(
            role="Regulatory Data Ingestion",
            backstory="Responsible for consuming regulatory data.",
            goal="Read a folder and consume knowledge from all the regulatory documents.",
            tools=[self.regulatory_tool.read_regulatory_docs],
            verbose=True,
        )

    def data_mapping_agent(self):
        return Agent(
            role="Data Mapping",
            backstory="Aligns ingested data with regulatory requirements.",
            goal="Map data from ingestion output using regulatory knowledge.",
            tools=[],
            verbose=True,
        )

    def validation_agent(self):
        return Agent(
            role="Data Validation",
            backstory="Ensures data compliance with regulatory standards.",
            goal="Validate data against XML/XSD format specified by regulators.",
            tools=[],
            verbose=True,
        )

    def monitoring_agent(self):
        return Agent(
            role="Compliance Monitoring",
            backstory="Monitors and documents data compliance efforts.",
            goal="Draft a document providing information for each data column.",
            tools=[],
            verbose=True,
        )