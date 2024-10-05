import pandas as pd
# from database_connect import mongo_operation as mongo 
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os, sys
# from src.constants import *
# from src.exception import CustomException


class MongoIO:
    mongo_ins = None

    def __init__(self):
        if MongoIO.mongo_ins is None:
            mongo_db_url = 'mongodb+srv://ankit:cK10u1EZtJj4Jcvr@cluster0.0n6et.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
            if mongo_db_url is None:
                raise Exception(f"Environment key: {mongo_db_url} is not set.")

            # MongoIO.mongo_ins = mongo(client_url=mongo_db_url,database_name=MONGO_DATABASE_NAME)
            MongoIO.mongo_ins = MongoClient(mongo_db_url)
            # MongoIO.mongo_ins["myntra-reviews"]
        self.mongo_ins = MongoIO.mongo_ins

    def store_reviews(self,product_name:str,reviews:pd.DataFrame):

        try:
            collection_name = product_name.replace(" ", "_")
            # self.mongo_ins.bulk_insert(reviews,collection_name)
            self.mongo_ins["myntra-reviews"][collection_name].insert_many(reviews.to_dict)
            # self.mongo_ins.bulk_write(reviews,collection_name)
            print(f"Reviews stored successfully for product: {product_name}")
            
        except Exception as e:
            print(f"Error in storing reviews: {e}")
            # raise CustomException(e, sys)


    def get_reviews(self,
                    product_name: str):
        try:
            data = self.mongo_ins.find(
                collection_name=product_name.replace(" ", "_")
            )

            return data

        except Exception as e:
            print(e)
            # raise CustomException(e, sys)


if __name__ == "__main__":
    obj = MongoIO()

