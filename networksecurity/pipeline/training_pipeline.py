import os
import sys
from networksecurity.exception.exception import networksecurityexception
from networksecurity.logging.logger import logging

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import datavalidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer

from networksecurity.entity.config_entity import(
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig,
    TrainingPipelineConfig,
)

from networksecurity.entity.artifact_entity import(
    dataingestionartifact,
    datavalidationartifact,
    DataTransformationArtifact,
    ModelTrainerArtifact,
) 

class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config=TrainingPipelineConfig()

    def start_data_ingestion(self):
        try:
            self.data_ingestion_config=DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("start data ingestion")
            data_ingestion=DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
            logging.info(f"data ingestion completed and artifact:{data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise networksecurityexception(e,sys)
        
    def start_data_validation(self,data_ingestion_artifact:dataingestionartifact):
        try:
            data_validation_config=DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            data_validatation=datavalidation(data_ingestion_artifact=data_ingestion_artifact,data_validation_config=data_validation_config)
            logging.info("initiate the data validation")
            data_validatation_artifact=data_validatation.initiate_data_validation()
            return data_validatation_artifact
        except Exception as e:
            raise networksecurityexception(e,sys)
        
    def start_data_transformation(self,data_validation_artifact:datavalidationartifact):
        try:
            data_transformation_config=DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            data_transformation=DataTransformation(data_validation_artifact=data_validation_artifact,data_transformation_config=data_transformation_config)
            logging.info("initiate the data transformation")
            data_transformation_artifact=data_transformation.initiate_data_transformation()
            return data_transformation_artifact
        except Exception as e:
            raise networksecurityexception(e,sys)
        
    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact)->ModelTrainerArtifact:
        try:
            self.model_trainer_config:ModelTrainerConfig=ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            model_trainer=ModelTrainer(model_trainer_config=self.model_trainer_config,data_transformation_artifact=data_transformation_artifact)
            model_trainer_artifact=model_trainer.initiate_model_trainer()
            return model_trainer_artifact
        except Exception as e:
            raise networksecurityexception(e,sys)
        
    def run_pipeline(self):
        try:
            data_ingestion_artifact=self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact=self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact=self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
            return model_trainer_artifact
        except Exception as e:
            raise networksecurityexception(e,sys)