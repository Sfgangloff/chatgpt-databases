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

subject = "french history"
concept = "france"

prompt_template_evaluation = PromptTemplate(
            input_variables=["concept","subject"],
            template = 'Give me a number between 0 and 10 which evaluates the difficulty of understanding {concept} is, provided that I do not know it but I am familiar with {subject} in general.'
        )

prompt_template_prerequisites = PromptTemplate(
            input_variables=["concept","subject"],
            template = 'Give me a list of the most important concepts that I need in {subject} in order to understand before I can try to understand {concept}, provided that I do not know it but I am familiar with {subject} in general. Just give me the concepts and not explanations.'
        )

prompt_template_check = PromptTemplate(
            input_variables=["concept","subject"],
            template = 'You told me that {concept} is a concept related to {subject}. Are you sure that this exists and it is indeed related to {subject} ? Answer by yes or no.'
        )

prompt_template_classification = PromptTemplate(
            input_variables=["subject"],
            template = 'Give me a short list of types of concepts that the following topic involves: {subject}'
        )

prompt_template_tight = PromptTemplate(
            input_variables=["concept","subject"],
            template = 'Give me a number between 0 and 10 which reflects how general the concept {concept} is general within the following domain: {subject}'
        )

prompt_template_reduce = PromptTemplate(
            input_variables=["concept"],
            template = 'Extract from "{concept}" the technical terms. Give me only the terms separated by the symbol #.'
        )

prompt_template_ranking = PromptTemplate(
            input_variables=["subject","concept_list"],
            template = 'Order the following concepts by how general they are within {subject}: {concept_list}. Give me only the terms separated by the symbol #.'
        )

concept_list=["Polymerase chain reaction (PCR),ligase",
              "Central dogma","Homologous chromosomes","Karyotype","Topoisomerases","Histone",
              "Chromatine","Genome","Cell cycle"]

ranking_chain = LLMChain(llm=llm,prompt=prompt_template_ranking,output_key="explanation")
response = ranking_chain.invoke({"subject":"molecular biology","concept_list":concept_list})

eval_chain = LLMChain(llm=llm,prompt=prompt_template_evaluation,output_key="evaluation")
for concept in concept_list:
    response = eval_chain.invoke({"subject":"molecual biology","concept":concept})
    print(response)