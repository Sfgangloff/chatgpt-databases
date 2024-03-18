from langchain_openai import OpenAI
from output_types import Index
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from prompt_templates import PROMPT_TEMPLATES
from dotenv import load_dotenv

load_dotenv()

class PartIndex():
    def __init__(self,llm:OpenAI):
        self.llm = llm
        self.names = ["part_draft","index_draft","specific_index"]
        self.parser = PydanticOutputParser(pydantic_object=Index)

    def generate_part_draft(self,subject:str,
                            title:str):
        prompt = ChatPromptTemplate.from_template(template=PROMPT_TEMPLATES[self.names[0]]['template'])
        messages = prompt.format_messages(subject=subject,
                                          title=title)
        output = self.llm.invoke(messages)
        print("part_draft",output)
        return output

    def generate_index_draft(self,subject:str,
                             title:str):
        part_draft = self.generate_part_draft(subject=subject,
                                              title=title)
        prompt = ChatPromptTemplate.from_template(template=PROMPT_TEMPLATES[self.names[1]]["template"])
        messages = prompt.format_messages(subject=subject,
                                          title=title,
                                          text=part_draft)
        output = self.llm.invoke(messages)
        print("index_draft",output)
        return output
    
    def generate(self,subject:str,
                             title:str):
        format_instructions = self.parser.get_format_instructions()
        index_draft = self.generate_index_draft(subject=subject,
                                              title=title)
        prompt = ChatPromptTemplate.from_template(template=PROMPT_TEMPLATES[self.names[2]]["template"])
        messages = prompt.format_messages(title=title,
                                          word_list=index_draft,
                                          format_instructions=format_instructions)
        output = self.llm.invoke(messages)
        results = self.parser.parse(output.content)
        return results