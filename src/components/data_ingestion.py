import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from src.exception import CustomException
from src.logger import logger
from src.components.data_transformation import DataTransformation


class DataIngestionConfig:
    """
    Class to store configuration paths for data ingestion.
    """
    def __init__(self):
        # Define file paths for training, testing, and raw data
        self.train_data_path = os.path.join('artifacts', "train.csv")
        self.test_data_path = os.path.join('artifacts', "test.csv")
        self.raw_data_path = os.path.join('artifacts', "data.csv")

class DataIngestion:
    """
    Class to handle data ingestion: loading, splitting, and saving datasets.
    """
    def __init__(self):
        # Initialize the DataIngestionConfig to get paths
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        """
        Method to perform the data ingestion process.
        - Reads data from a CSV file
        - Splits data into training and testing sets
        - Saves the raw, training, and testing data to specified paths
        """
        logger.info("Entered the data ingestion method or component")
        try:
            # Load the dataset into a Pandas DataFrame
            df = pd.read_csv(os.path.join('notebook', 'data', 'stud.csv'))
            logger.info('Read the dataset as dataframe')

            # Create necessary directories if they do not exist
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            # Save the raw data to the specified path
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            logger.info("Raw data saved")

            # Split the data into training and testing sets
            logger.info("Train-test split initiated")
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            # Save the training data to the specified path
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            # Save the testing data to the specified path
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)
            logger.info("Ingestion of the data is completed")

            # Return the paths of the saved training and testing data
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            # Raise a custom exception if an error occurs
            raise CustomException(e, sys)

"""
if __name__=="__main__":
    dataobj = DataIngestion()
    train_path, test_path = dataobj.initiate_data_ingestion()
    
    datatransobj = DataTransformation()
    datatransobj.initiate_data_transformation(train_path, test_path)
"""
