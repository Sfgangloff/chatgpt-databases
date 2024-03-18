from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.agents import load_tools,initialize_agent
from langchain.agents import AgentType
from dotenv import load_dotenv

import re
import pandas as pd
import numpy as np

load_dotenv()

llm = OpenAI(temperature=0.1)

subject = "molecular biology"
concept = "research community"

prompt_template_explanation = PromptTemplate(
                    input_variables=["concept","subject"],
                    template = 'Explain me what {concept} is, within the following domain:{subject}'
                )

explanation_chain = LLMChain(llm=llm,prompt=prompt_template_explanation,output_key="explanation")

prompt_template_reduce = PromptTemplate(
            input_variables=["explanation","concept"],
            template = 'Extract from "{explanation}" the technical terms. Give me only the terms separated by the symbol #. Keep only the concepts which are simpler than {concept}.'
        )
reduce_chain = LLMChain(llm=llm,prompt=prompt_template_reduce,output_key="concept_list")

from langchain.chains import SequentialChain
overall_chain = SequentialChain(
    chains = [explanation_chain,reduce_chain],
    input_variables=["subject","concept"],
    output_variables=["concept_list"],
    verbose=True
)

response = overall_chain.invoke({"subject":subject,"concept":concept})
print(response)