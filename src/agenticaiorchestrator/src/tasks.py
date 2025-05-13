from crewai import Task
from textwrap import dedent

class RegulatoryTasks:
    def mapping_task(self, agent):
        return Task(
            description=dedent(
                f"""
                **Task**: Map Ingested Trade Data
                **Description**: Map ingested trade data to regulatory data column by column and generate a CSV.
                """),
            expected_output="CSV file named mapped_output.csv with mapped data.",  # Add this line
            agent=agent,
        )

    def validation_task(self, agent):
        return Task(
            description=dedent(
                f"""
                **Task**: Validate Mapped Data
                **Description**: Validate mapped data against XML/XSD format required by regulators.
                """),
            expected_output="Validation status indicating success or failure.",  # Ensure this line is present
            agent=agent,
        )

    def compliance_monitoring_task(self, agent):
        return Task(
            description=dedent(
                f"""
                **Task**: Draft Compliance Monitoring Document
                **Description**: Draft a document providing information about each data column.
                """),
            expected_output="Text document named monitoring_report.txt with column info.",  # Ensure this line is present
            agent=agent,
        )