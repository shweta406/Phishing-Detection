from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import datavalidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.exception.exception import networksecurityexception
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig
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
        data_transformation_config=DataTransformationConfig(trainingpipelineconfig)
        data_transformation=DataTransformation(data_validatation_artifact,data_transformation_config)
        logging.info("initiate the data transformation")
        data_transformation_artifact=data_transformation.initiate_data_transformation()
        logging.info("data transformation completed")
        print(data_transformation_artifact)


        logging.info("Model Transformation Completed")
        model_trainer_config=ModelTrainerConfig(trainingpipelineconfig)
        model_trainer=ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact=model_trainer.initiate_model_trainer()
        logging.info("model training artifact created")
    except Exception as e:
        raise networksecurityexception(e,sys)