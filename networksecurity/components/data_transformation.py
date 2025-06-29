import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constant.training_pipeline import TARGET_COLUMN
from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from networksecurity.entity.artifact_entity import(
    DataTransformationArtifact,
    datavalidationartifact
)
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.exception.exception import networksecurityexception
from networksecurity.logging.logger import logging
from networksecurity.utils.main_utils.utils import save_numpy_array_data,save_object

class DataTransformation:
    def __init__(self,data_validation_artifact:datavalidationartifact,
                 data_transformation_config:DataTransformationConfig):
        
        try:
            self.data_validation_artifact:datavalidationartifact=data_validation_artifact
            self.data_transformation_config:DataTransformationConfig=data_transformation_config
        except Exception as e:
            raise networksecurityexception(e,sys)
        
    @staticmethod
    def read_data(file_path)-> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise networksecurityexception(e,sys)
        
    def get_data_transformer_object(cls)->Pipeline:
        '''
        it initiates a knnimputer object with the parameters specified in the training_pipeline.py file
        and returns a pipeline object with the knnimputer object as first step
        
        args: 
        cls:datatransformation
        
        returns: 
        a pipeline object'''

        logging .info(
            "entered  get_data_transformer_object method of transformation class"
        )
        #whatever parameters we are giving is considered as key value pair
        try:
           imputer:KNNImputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
           logging.info(
               f"initialise knnimputer with{DATA_TRANSFORMATION_IMPUTER_PARAMS}"
           )
           processor:Pipeline=Pipeline([("imputer",imputer)])
           return processor
        except Exception as e:
            raise networksecurityexception(e,sys)
        
    def initiate_data_transformation(self)->DataTransformationArtifact:
        logging.info("entered initiate_data_transformation method of datatransformation class")
        try:
            logging.info("starting data transformation")
            train_df=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            
            ##training dataframe

            input_feature_train_df=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            taget_feature_train_df=train_df[TARGET_COLUMN]
            taget_feature_train_df=taget_feature_train_df.replace(-1,0)

            ##testing dataframe

            input_feature_test_df=test_df.drop(columns=[TARGET_COLUMN],axis=1)
            taget_feature_test_df=test_df[TARGET_COLUMN]
            taget_feature_test_df=taget_feature_test_df.replace(-1,0)

            preprocessor=self.get_data_transformer_object()

            preprocessor_object=preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature=preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_feature=preprocessor_object.transform(input_feature_test_df)

            train_arr=np.c_[transformed_input_train_feature,np.array(taget_feature_train_df)]
            test_arr=np.c_[transformed_input_test_feature,np.array(transformed_input_test_feature)]

            #save numpy array data
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,array=train_arr,)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,array=test_arr,)
            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor_object,)

            #preparing artifacts

            data_transformation_artifact=DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_test_file_path
            )
            return data_transformation_artifact


        except Exception as e:
            raise networksecurityexception(e,sys)