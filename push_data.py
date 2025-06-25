import os
import sys
import json

from dotenv import load_dotenv
import pymongo.mongo_client #to call all the env variables nd we require these env var so we know that where we have to push the data
load_dotenv()

mongo_db_url=os.getenv("MONGO_DB_URL")
print(mongo_db_url)

import certifi #to know that it is valid certificate like when we try to bulid connection so using this lib they know that it is valid certificate aur request
ca=certifi.where()#trusted certificate authority

import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import networksecurityexception
from networksecurity.logging.logger import logging

class networkdataextract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise networksecurityexception(e,sys)
        

    def csv_to_json_convertor(self,file_path):
        try:
            data=pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            records=list(json.loads(data.T.to_json()).values())#transpose jisse same format me rhe json .. .values for key value pair ....this is list of json is liye list
            return records

        except Exception as e:
            raise networksecurityexception(e,sys)
        
    def insert_data_mongodb(self,records,database,collection): #records kon se push kr rhe ..database.. collection is table in sql
        try:
            self.database=database
            self.collection=collection
            self.records=records

            self.mongo_client=pymongo.MongoClient(mongo_db_url)#to establish relation between mongodb and python
            self.database=self.mongo_client[self.database]
            self.collection=self.database[self.collection]
            self.collection.insert_many(self.records)
            return(len(self.records))
        except Exception as e:
            raise networksecurityexception(e,sys)
        
if __name__=='__main__':
    file_path="Network_Data\phisingData.csv"
    database="shweta"
    collection="networkdata"
    networkobj=networkdataextract()
    records=networkobj.csv_to_json_convertor(file_path=file_path)
    print(records)
    no_of_records=networkobj.insert_data_mongodb(records,database,collection)
    print(no_of_records)
