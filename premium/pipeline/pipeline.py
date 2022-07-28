
from premium.exception import PremiumException
from premium.entity.artifact_entity import *
from premium.entity.config_entity import *
from premium.logger import logging
from premium.config.configuration import Configuration
from premium.component.data_ingestion import DataIngestion


from threading import Thread


class pipeline(Thread):
    
    def __init__(self,config: Configuration):
        try:
            pass
        except Exception as e:
            raise PremiumException(e,sys) from e

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            data_ingestion = DataIngestion(data_ingestion_config = self.config.get_data_ingestion_config())
            return data_ingestion.initiate_data_ingestion()

        except Exception as e:
            raise PremiumException(e, sys) from e
