from langchain_openai import OpenAI
from output_types import Index
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from prompt_templates import PROMPT_TEMPLATES
from dotenv import load_dotenv

load_dotenv()

class Part():
    def __init__(self,llm:OpenAI):
        self.llm = llm
        self.names = ["part","part_reduce"]

    def generate(self,subject:str,
                      title:str,
                      index:str):
        prompt = ChatPromptTemplate.from_template(template=PROMPT_TEMPLATES[self.names[0]]['template'])
        messages = prompt.format_messages(subject=subject,
                                          title=title,
                                          index=index)
        content = self.llm.invoke(messages)

        prompt = ChatPromptTemplate.from_template(template=PROMPT_TEMPLATES[self.names[1]]["template"])
        messages = prompt.format_messages(content=content)
        output = self.llm.invoke(messages)
        return output