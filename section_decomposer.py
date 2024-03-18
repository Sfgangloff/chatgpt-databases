from langchain_openai import OpenAI
from output_types import Section
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from prompt_templates import PROMPT_TEMPLATES
from dotenv import load_dotenv

load_dotenv()

class SectionDecomposer():
    def __init__(self,llm:OpenAI):
        self.llm = llm
        self.names = ["decompose_sections"]
        self.parser = PydanticOutputParser(pydantic_object=Section)

    def generate(self,subject:str,
                      section_title:str,
                      subsection_title:str,
                      subsections_titles:str):
        format_instructions = self.parser.get_format_instructions()
        prompt = ChatPromptTemplate.from_template(template=PROMPT_TEMPLATES[self.names[0]]['template'])
        messages = prompt.format_messages(subject=subject,
                                          section_title=section_title,
                                          subsection_title=subsection_title,
                                          subsections_titles=subsections_titles,
                                          format_instructions=format_instructions)
        output = self.llm.invoke(messages)
        results = self.parser.parse(output.content)
        return results