from setuptools import setup, find_packages

setup(
    name="agenticaiorchestrator",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'crewai',
        'PyPDF2',
        'PyYAML',
        'requests',
        'pydantic',
        'langchain',
        'openai'
    ],
)