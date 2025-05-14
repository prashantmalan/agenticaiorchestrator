from crewai import Crew
from textwrap import dedent
from agents import RegulatoryAgents
from tasks import RegulatoryTasks
from dotenv import load_dotenv
from langchain.llms import OpenAI
import os
from crewai_tools import XMLSearchTool
from tools.regulatory_data_tool import RegulatoryTools
from tools.fpml_data_tool import FPMLDataTools
load_dotenv()

class ComplianceCrew:
    def __init__(self):
        self.llm = OpenAI(
            model="gpt-4.1-nano",
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.5
        )
        self.agents = RegulatoryAgents(self.llm)
        self.tasks = RegulatoryTasks()
        self.fpml_tool = FPMLDataTools()  # Initialize FpmlDataTool
        self.regulatory_tool = RegulatoryTools()  # Initialize RegulatoryDataTool

    def process_fpml_data(self):
        """Process FpML data using FpmlDataTool."""
        fpml_url = "https://www.fpml.org/spec/fpml-5-3-6-rec-1/html/confirmation/xml/products/interest-rate-derivatives/ird-ex01-vanilla-swap.xml"
        fpml_data = self.fpml_tool.read(fpml_url)
        print("FpML Data Processed:", fpml_data)
        return fpml_data

    def process_regulatory_data(self):
        """Process regulatory data using RegulatoryDataTool."""
        regulatory_docs_path = r"C:\Users\user\Downloads\AIDG_v2_0.zip"
        regulatory_data = self.regulatory_tool.read(regulatory_docs_path)
        print("Regulatory Data Processed:", regulatory_data)
        return regulatory_data

    def run(self):
        # Process FpML and regulatory data
        fpml_data = self.process_fpml_data()
        regulatory_data = self.process_regulatory_data()

        # Initialize agents
        trade_data_ingestion_agent = self.agents.trade_data_ingestion_agent()
        regulatory_data_ingestion_agent = self.agents.regulatory_data_ingestion_agent()
        data_mapping_agent = self.agents.data_mapping_agent()
        # Initialize tasks
        trade_data_ingestion_task = self.tasks.trade_data_ingestion_task(trade_data_ingestion_agent)
        regulatory_data_ingestion_task = self.tasks.regulatory_data_ingestion_task(regulatory_data_ingestion_agent)

        # Create Crew instance
        crew = Crew(
            agents=[
                trade_data_ingestion_agent,
                regulatory_data_ingestion_agent, 
                data_mapping_agent
            ],
            tasks=[
                trade_data_ingestion_task,
                regulatory_data_ingestion_task
            ],
            llm=self.llm,
            verbose=True
        )

        # Kickoff the crew process
        result = crew.kickoff()
        return result

if __name__ == "__main__":
    print("## Welcome to Compliance Crew")
    print('-------------------------------')
    compliance_crew = ComplianceCrew()
    result = compliance_crew.run()
    print("\n\n########################")
    print("## Compliance Process Result")
    print("########################\n")
    print(result)