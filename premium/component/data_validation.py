from premium.exception import PremiumException
from premium.logger import logging
import os,sys
import pandas as pd
from premium.entity.config_entity import DataValidationConfig
from premium.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab
from premium.util.util import read_yaml_file
import json

class DataValidation:
    def __init__(self, data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig) -> None:

        try:
            logging.info(f"{'='*30}Data Valdaition log started.{'='*30} \n")
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
        
        except Exception as e:
            raise PremiumException(e,sys) from e


    def get_train_and_test_df(self):
        try:
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            return train_df, test_df

        except Exception as e:
            raise PremiumException(e,sys) from e


    def is_train_test_file_exist(self) -> bool:
        try:
            logging.info("Checking if training and test file is available")
            is_train_file_exist = False
            is_test_file_exist = False

            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            is_train_file_exist = os.path.exists(train_file_path)
            is_test_file_exist = os.path.exists(test_file_path)

            is_available =  is_train_file_exist and is_test_file_exist

            logging.info(f"Is train and test file exists? -> {is_available}")

            if is_available == False:
                traing_file_path = self.data_ingestion_artifact.train_file_path
                testing_file_path = self.data_ingestion_artifact.test_file_path
                message = f'Training file {traing_file_path} and Testing file {testing_file_path} not exist'
                raise Exception(message)

        except Exception as e:
            raise PremiumException(e,sys) from e

    
    def validate_dataset_schema(self) -> bool:
        try:
            validation_status = False
            
            schema_file_path = self.data_validation_config.schema_file_path
            schema_data = read_yaml_file(file_path=schema_file_path)
            schema_columns = schema_data['columns']
            schema_datatype_dataframe = pd.DataFrame.from_dict(schema_columns,orient='index')

            train_file_path = self.data_ingestion_artifact.train_file_path
            train_df = pd.read_csv(train_file_path)

            test_file_path = self.data_ingestion_artifact.test_file_path
            test_df = pd.read_csv(test_file_path)

            train_datatype_dataframe = pd.DataFrame(train_df.dtypes)
            test_datatype_dataframe = pd.DataFrame(test_df.dtypes)

            if schema_datatype_dataframe.equals(train_datatype_dataframe) :
                if schema_datatype_dataframe.equals(test_datatype_dataframe):
                    validation_status = True
                    logging.info("validate dataset schema is good to go!!")
                else :
                    logging.info("Validate dataset schema failed")
            else :
                logging.info("Validate dataset schema failed")
            
                
            #validation_status = True
            return validation_status

        except Exception as e:
            raise PremiumException(e,sys) from e


    def get_and_save_data_drift_report(self):
        try:
            profile = Profile(sections=[DataDriftProfileSection()])

            train_df,test_df = self.get_train_and_test_df()

            profile.calculate(train_df,test_df)

            report = json.loads(profile.json())

            report_file_path = self.data_validation_config.report_file_path
            report_dir = os.path.dirname(report_file_path)
            os.makedirs(report_dir,exist_ok=True)

            with open(report_file_path, "w") as report_file:
                json.dump(report, report_file, indent=6)
            return report

        except Exception as e:
            raise PremiumException(e,sys) from e


    def save_data_drift_report_page(self):
        try:
            dashboard = Dashboard(tabs=[DataDriftTab()])
            train_df,test_df = self.get_train_and_test_df()
            dashboard.calculate(train_df,test_df)

            report_page_file_path = self.data_validation_config.report_page_file_path
            report_page_dir = os.path.dirname(report_page_file_path)
            os.makedirs(report_page_dir, exist_ok = True)
            dashboard.save(report_page_file_path)

        except Exception as e:
            raise PremiumException(e,sys) from e


    def is_data_drift_found(self)->bool:
        try:
            report = self.get_and_save_data_drift_report()
            self.save_data_drift_report_page()
            return True

        except Exception as e:
            raise PremiumException(e,sys) from e


    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            self.is_train_test_file_exist()
            self.validate_dataset_schema()
            self.is_data_drift_found()

            data_validation_artifact = DataValidationArtifact(
                schema_file_path = self.data_validation_config.schema_file_path,
                report_file_path = self.data_validation_config.report_file_path,
                report_page_file_path = self.data_validation_config.report_page_file_path,
                is_validated = True,
                message = f"Data Validation performed successully.")

            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact

        except Exception as e:
            raise PremiumException(e,sys) from e


    def __del__(self):
        logging.info(f"{'='*20}Data Valdaition log completed.{'='*20} \n\n")