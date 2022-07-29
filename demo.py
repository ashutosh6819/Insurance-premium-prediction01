from premium.pipeline.pipeline import Pipeline
from premium.exception import PremiumException
from premium.logger import logging
from premium.config.configuration import Configuration
import os,sys

from sklearn import pipeline

def main():
    try:
        config_path = os.path.join("config","config.yaml")
        pipeline = pipeline(Configuration(config_file_path=config_path))
        pipeline.start()
        logging.info("main function")

    except Exception as e:
        raise PremiumException(e,sys) from e

if __name__=="__main__":
    main()