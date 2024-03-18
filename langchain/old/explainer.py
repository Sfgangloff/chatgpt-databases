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

class Explainer():
    def __init__(self,llm:OpenAI):
        self.llm = llm

    def file_path(self,subject:str):
        return "csv_files/"+ subject.lower().replace(" ","_") + ".csv"

    def get_df(self,subject:str):
        df = pd.read_csv(self.file_path(subject))
        return df

    def generate_explanation(self,concept:str,
                              subject:str):

        accessory_part = "."
        if subject !="":
            accessory_part = f" and in relation with {subject}"
        prompt_template_explanation = PromptTemplate(
                    input_variables=["concept","subject"],
                    template = 'Explain me what {concept} is in itself'+accessory_part
                )

        explanation_chain = LLMChain(llm=llm,prompt=prompt_template_explanation,output_key="explanation")
        response = explanation_chain.invoke({"concept":concept,"subject":subject})
        return response["explanation"]
    
    def apply(self,subject:str):
        df = self.get_df(subject)
        if "EXPLANATION" not in df.columns:
            df["EXPLANATION"] = ""
        df["EXPLANATION"] = df["EXPLANATION"].fillna("")
        df_without_expl = df.loc[df["EXPLANATION"]==""]
        concept = df_without_expl["CONCEPT"].values[1]
        parent = df_without_expl["PARENT"].values[1]
        explanation = self.generate_explanation(concept=concept,
                                                subject=parent)
        explanation = explanation.replace("\n"," ")
        df.loc[df["CONCEPT"]==concept,"EXPLANATION"]=explanation
        df.to_csv(self.file_path(subject),index=False)
