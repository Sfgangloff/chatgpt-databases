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

class Updater():
    def __init__(self,llm:OpenAI,
                 width:int):
        self.llm = llm
        self.width = width
        
    def file_path(self,subject:str):
        return "csv_files/"+ subject.lower().replace(" ","_") + ".csv"
    
    def get_df(self,subject:str):
        with open(self.file_path(subject),"r+") as file:
            text = file.read()
            print(text)
            if text == "":
                file.write(f"CONCEPT,RANK,PARENT,LOCK\n{subject},0,,0")
        df = pd.read_csv(self.file_path(subject))
        return df
    
    def construct_base_df(self):
        return pd.DataFrame(columns=[
                                      "CONCEPT",
                                      "RANK",
                                      "PARENT",
                                      "LOCK"])

    def current_rank(self,df:pd.DataFrame):
        df_unlocked = df.loc[df["LOCK"]!=1]
        return df_unlocked["RANK"].min()
    
    def current_root(self,df:pd.DataFrame):
        rank = self.current_rank(df=df)
        lock_df = df.loc[(df["RANK"]==rank) * (df["LOCK"]!=1)]
        root = lock_df["CONCEPT"].values[0]
        return root

    def generate_subject_concepts(self,subject:str,
                                  df:pd.DataFrame):
        
        # listed_concepts = set(df["CONCEPT"].values)

        prompt_template_concepts = PromptTemplate(
            input_variables=["subject"],
            template = 'I want to learn about {subject}. List ten concepts related to {subject}.'
        )

        concepts_chain = LLMChain(llm=self.llm,prompt=prompt_template_concepts,output_key="concept_list")
        response = concepts_chain.invoke({"subject":subject})
        return response["concept_list"]
    
    def post_precess_response(self,text:str):
        regex_pattern="\s*\n+\d+\.\s*"
        concept_list = re.split(regex_pattern,text)
        concept_list = [item for item in concept_list if item!=""]
        return concept_list
    
    def generate_concept_list(self,df:pd.DataFrame,
                              subject:str):
        text = self.generate_subject_concepts(subject = subject,
                                              df=df)

        concept_list = self.post_precess_response(text)
        return concept_list
    
    def compute_df(self,df:pd.DataFrame,
                      concept_list:list[str]):
        concept_list = [concept for concept in concept_list if concept not in df["CONCEPT"].values]
        new_df = pd.DataFrame(concept_list,columns=["CONCEPT"])
        new_df = pd.concat([new_df,df],axis=0)
        new_df["RANK"]=0
        new_df["PARENT"]=np.nan
        return new_df
    
    def halt_criterion(self,df:pd.DataFrame,
                       concept_list:list[str]):
        criterion = all(concept in df["CONCEPT"].values for concept in concept_list)
        return criterion
    
    def reduce(self,concept:str):
        prompt_template_reduce = PromptTemplate(
            input_variables=["concept"],
            template = 'Extract from "{concept}" the technical terms. Give me only the terms separated by the symbol #.'
        )

        reduce_chain = LLMChain(llm=self.llm,prompt=prompt_template_reduce,output_key="concept_list")
        response = reduce_chain.invoke({"concept":concept})
        return response["concept_list"]

    def apply(self,subject:str):
        df = self.get_df(subject=subject)
        rank = self.current_rank(df)
        root = self.current_root(df)
        new_df = self.construct_base_df()
        for _ in range(self.width):
            concept_list = self.generate_concept_list(df=new_df,
                                                              subject=root)
            new_list = []
            for concept in concept_list:
                new_list.extend(self.reduce(concept).split('#'))
            concept_list=new_list
            concept_list = [concept.replace('\n','').replace('"','').strip().lower() for concept in concept_list]
            halt_criterion = self.halt_criterion(df=new_df,
                                                 concept_list=concept_list)
            if halt_criterion:
                break
            else:
                new_df = self.compute_df(df=new_df,concept_list=concept_list)
        new_df["RANK"]=rank+1
        new_df["PARENT"]=root
        new_df["LOCK"]=0
        df = pd.concat([df,new_df],axis=0)
        df.loc[df["CONCEPT"]==root,"LOCK"]=1
        df.to_csv(self.file_path(subject),index=False)
    