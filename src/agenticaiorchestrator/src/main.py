from crewai import Crew
from textwrap import dedent
from agents import RegulatoryAgents
from tasks import RegulatoryTasks
from dotenv import load_dotenv

load_dotenv()

class ComplianceCrew:
    def __init__(self):
        self.agents = RegulatoryAgents()
        self.tasks = RegulatoryTasks()

    def run(self):
        # Define your custom agents and tasks here
        trade_data_ingestion_agent = self.agents.trade_data_ingestion_agent()
        regulatory_data_ingestion_agent = self.agents.regulatory_data_ingestion_agent()
        data_mapping_agent = self.agents.data_mapping_agent()
        validation_agent = self.agents.validation_agent()
        monitoring_agent = self.agents.monitoring_agent()

        # Custom tasks include agent name and variables as input
        mapping_task = self.tasks.mapping_task(data_mapping_agent)
        validation_task = self.tasks.validation_task(validation_agent)
        compliance_monitoring_task = self.tasks.compliance_monitoring_task(monitoring_agent)

        # Define your custom crew here
        crew = Crew(
            agents=[
                trade_data_ingestion_agent,
                regulatory_data_ingestion_agent,
                data_mapping_agent,
                validation_agent,
                monitoring_agent
            ],
            tasks=[
                mapping_task,
                validation_task,
                compliance_monitoring_task
            ],
            verbose=True,
        )

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