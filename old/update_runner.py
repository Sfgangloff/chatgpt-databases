from updater import Updater
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

class UpdateRunner():
    def __init__(self,
                 updater:Updater,
                 subject_list:list[str],
                 max_rank:int):
        self.updater = updater
        self.subject_list = subject_list
        self.halt_information = {}
        self.max_rank = max_rank

    def run_single(self,n:int,
            subject:str,
            df:pd.DataFrame=None):
        # if df is None:
        df = self.updater.get_df(subject=subject)
        for _ in range(n):
            concept_list = self.updater.generate_concept_list(df=df,
                                                              subject=subject)
            halt_criterion = self.updater.halt_criterion(df=df,
                                                         concept_list=concept_list)
            if halt_criterion:
                self.halt_information[subject] = _
                break
            else:
                df = self.updater.compute_df(df=df,concept_list=concept_list)
        return df
    
    def run(self,n:int):
        for subject in self.subject_list:
            df = self.run_single(n=n,subject=subject)
            self.updater.save(df=df,file_path=self.updater.file_path(subject=subject))
    # def run(self,n:int):
    #     for subject in self.subject_list:
    #         df = self.run_single(n=n,subject=subject)
    #         for rank in range(1,self.max_rank+1):
    #             concepts = set(df.loc[df["RANK"]==rank-1]["CONCEPT"].values)
    #             for concept in concepts:
    #                 new_df = self.run_single(n=n,subject=concept,
    #                                          df=pd.DataFrame(columns=["CONCEPT","RANK","PARENT"]))
    #                 new_df["RANK"]=rank
    #                 new_df["PARENT"] = concept
    #                 df.loc[df["CONCEPT"]==concept,"LOCK"]=1
    #                 df = pd.concat([df,new_df],axis=0)
    #         self.updater.save(df=df,file_path=self.updater.file_path(subject=subject))
