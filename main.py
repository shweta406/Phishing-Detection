from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import datavalidation
from networksecurity.exception.exception import networksecurityexception
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
import sys

if __name__=='__main__':
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
        data_ingestion=DataIngestion(dataingestionconfig)
        logging.info("initiate the data ingestion")
        dataingestionartifact=data_ingestion.initiate_data_ingestion()
        logging.info("data initiation completed")
        print(dataingestionartifact)
        data_validation_config=DataValidationConfig(trainingpipelineconfig)
        data_validatation=datavalidation(dataingestionartifact,data_validation_config)
        logging.info("initiate the data validation")
        data_validatation_artifact=data_validatation.initiate_data_validation()
        logging.info("data validation completed")
        print(data_validatation_artifact)
    except Exception as e:
        raise networksecurityexception(e,sys)