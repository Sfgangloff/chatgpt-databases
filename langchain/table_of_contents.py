from langchain_openai import OpenAI
from output_types import Document
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from prompt_templates import PROMPT_TEMPLATES
from dotenv import load_dotenv

load_dotenv()

class TableOfContents():
    def __init__(self,llm:OpenAI):
        self.llm = llm
        self.names = ["table_of_contents"]
        self.parser = PydanticOutputParser(pydantic_object=Document)

    def generate(self,subject:str):
        format_instructions = self.parser.get_format_instructions()
        prompt = ChatPromptTemplate.from_template(template=PROMPT_TEMPLATES[self.names[0]]["template"])
        messages = prompt.format_messages(subject=subject,format_instructions=format_instructions)
        output = self.llm.invoke(messages)
        results = self.parser.parse(output.content)
        return results
