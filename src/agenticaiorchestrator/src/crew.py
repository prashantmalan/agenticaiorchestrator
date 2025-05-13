from crewai import Crew, Agent, Task
from langchain.llms import OpenAI
import yaml
import os
import logging
from dotenv import load_dotenv
from tools.regulatory_data_tool import RegulatoryDataTool
from tools.fpml_data_tool import FPMLDataTool
import pandas as pd

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)
logging.getLogger('LiteLLM').setLevel(logging.WARNING)  # Set to WARNING to suppress DEBUG logs

#logger = logging.getLogger(__name__)
class ComplianceCrew:
    def __init__(self):
        self.llm = OpenAI(
            model="gpt-4.1-nano",
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.5
        
        )
        self.regulatory_tool = RegulatoryDataTool()
        self.fpml_tool = FPMLDataTool()
        self.load_configurations()
        self.setup_agents()
        self.setup_tasks()
        self.crew = Crew(
            agents=list(self.agents.values()),
            tasks=list(self.tasks.values()),
            llm=self.llm
        )

    def load_configurations(self):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            agents_path = os.path.join(current_dir, 'config', 'agents.yaml')
            tasks_path = os.path.join(current_dir, 'config', 'tasks.yaml')
            
            logger.info(f"Looking for agents.yaml at: {agents_path}")
            logger.info(f"Looking for tasks.yaml at: {tasks_path}")
            
            with open(agents_path, 'r') as file:
                self.agents_config = yaml.safe_load(file)['agents']

            with open(tasks_path, 'r') as file:
                self.tasks_config = yaml.safe_load(file)['tasks']
                
            logger.info("Successfully loaded configurations")
        except Exception as e:
            logger.error(f"Error loading configurations: {str(e)}")
            raise

    def setup_agents(self):
        try:
            self.agents = {}
            for agent_id, config in self.agents_config.items():
                self.agents[agent_id] = Agent(
                    name=agent_id,
                    role=config['role'],
                    goal=config['goal'],
                    backstory=config['backstory'],
                    verbose=True,
                    allow_delegation=False,
                    llm=self.llm
                )
            logger.info("Successfully set up agents")
        except Exception as e:
            logger.error(f"Error setting up agents: {str(e)}")
            raise

    def setup_tasks(self):
        try:
            self.tasks = {}
            for task_id, config in self.tasks_config.items():
                execution_function = None
                if task_id == "data_ingestion_task":
                    execution_function = self.data_ingestion_task_execution
                elif task_id == "mapping_task":
                    execution_function = self.mapping_task_execution
                elif task_id == "validation_task":
                    execution_function = self.validation_task_execution
                elif task_id == "compliance_monitoring_task":
                    execution_function = self.monitoring_task_execution

                self.tasks[task_id] = Task(
                    name=task_id,
                    description=config['description'],
                    expected_output=config['expected_output'],
                    agent=self.agents[config['agent']],
                    execution_function=execution_function
                )
            logger.info("Successfully set up tasks")
        except Exception as e:
            logger.error(f"Error setting up tasks: {str(e)}")
            raise

    def data_ingestion_task_execution(self, task):
        try:
            logger.debug("Starting data ingestion task execution")
            fpml_data = self.fpml_tool.get_registry().get('trades', [])
            if not fpml_data:
                logger.error("No FPML data found")
                return "No data to ingest"
            df = pd.DataFrame(fpml_data)
            df.to_csv("ingestion_output.csv", index=False)
            logger.info("FPML data ingested and CSV created successfully")
            return "Data ingestion completed"
        except Exception as e:
            logger.error(f"Error executing data ingestion task: {str(e)}")
            raise

    def mapping_task_execution(self, task):
        try:
            logger.debug("Starting mapping task execution")
            df = pd.read_csv("ingestion_output.csv")
            logger.debug(f"Data before mapping: {df.head()}")
            mapped_df = df.rename(columns={
                "TradeDate": "Regulatory_Trade_Date",
                "Counterparty": "Regulatory_Counterparty",
                "Notional": "Regulatory_Notional"
            })
            mapped_df.to_csv("mapped_output.csv", index=False)
            logger.info("Data mapping completed and CSV created successfully")
            return "Mapping completed"
        except Exception as e:
            logger.error(f"Error executing mapping task: {str(e)}")
            raise

    def validation_task_execution(self, task):
        try:
            logger.debug("Starting validation task execution")
            df = pd.read_csv("mapped_output.csv")
            validation_passed = all(df.columns == ["Regulatory_Trade_Date", "Regulatory_Counterparty", "Regulatory_Notional"])
            validation_result = "Validation successful" if validation_passed else "Validation failed"
            logger.info(validation_result)
            return validation_result
        except Exception as e:
            logger.error(f"Error executing validation task: {str(e)}")
            raise

    def monitoring_task_execution(self, task):
        try:
            logger.debug("Starting monitoring task execution")
            df = pd.read_csv("mapped_output.csv")
            column_info = df.dtypes.to_dict()
            with open("monitoring_report.txt", "w") as file:
                for column, dtype in column_info.items():
                    file.write(f"Column: {column}, Type: {dtype}\n")
            logger.info("Monitoring document drafted successfully")
            return "Monitoring document drafted"
        except Exception as e:
            logger.error(f"Error executing monitoring task: {str(e)}")
            raise

    def run_workflow(self):
        try:
            logger.info("Starting workflow execution...")
            self.regulatory_tool.read_regulatory_docs("regulatory_docs_path")
            result = self.crew.kickoff()
            logger.info("Workflow completed successfully")
            return result
        except Exception as e:
            logger.error(f"Error during workflow execution: {str(e)}")
            raise