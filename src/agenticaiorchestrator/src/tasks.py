from crewai import Task
from textwrap import dedent

class RegulatoryTasks:
    def trade_data_ingestion_task(self, agent):
        return Task(
            description=dedent("""
                **Task**: Ingest FPML data and generate a CSV with column names and values.
            """),
            expected_output="CSV file named ingestion_output.csv with FPML data.",
            agent=agent
        )
    def regulatory_data_ingestion_task(self, agent):
        return Task(
            description=dedent("""
                **Task**: Consume regulatory docs from folder and build the knowledge base.
            """),
            expected_output="CSV file with a list of columns needed for regulatory requirements and their validation rules.",
            agent=agent
        )

    def mapping_task(self, agent):
        return Task(
            description=dedent("""
                **Task**: Map ingested trade data to regulatory data column by column and generate a CSV.
            """),
            expected_output="CSV file named mapped_output.csv with mapped data.",
            agent=agent
        )

    def validation_task(self, agent):
        return Task(
            description=dedent("""
                **Task**: Validate mapped data against XML/XSD format required by regulators.
            """),
            expected_output="Validation status indicating success or failure.",
            agent=agent
        )

    def compliance_monitoring_task(self, agent):
        return Task(
            description=dedent("""
                **Task**: Draft a document providing information about each data column.
            """),
            expected_output="Text document named monitoring_report.txt with column info.",
            agent=agent
        )