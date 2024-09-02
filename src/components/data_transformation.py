import os
import sys
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from src.exception import CustomException
from src.logger import logger
from src.utils import save_object

class DataTransformation:
    def __init__(self):
        # Path to save the preprocessor object after transformation
        self.preprocessor_obj_file_path = os.path.join('artifacts', "preprocessor.pkl")

    def get_data_transformer_object(self):
        """
        This function is responsible for creating and returning the data transformation pipeline.
        The pipeline includes:
        - Imputation of missing values
        - Scaling of numerical features
        - Encoding of categorical features
        """
        try:
            # List of numerical columns to be processed
            numerical_columns = ["writing_score", "reading_score"]
            # List of categorical columns to be processed
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

            # Pipeline for numerical columns: handles missing values and scaling
            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),  # Impute missing values with median
                    ("scaler", StandardScaler())  # Standardize the numerical features
                ]
            )

            # Pipeline for categorical columns: handles missing values, encoding, and scaling
            cat_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),  # Impute missing values with the most frequent value
                    ("one_hot_encoder", OneHotEncoder()),  # One-hot encode categorical features
                    ("scaler", StandardScaler(with_mean=False))  # Scale encoded features (without centering)
                ]
            )

            # Logging the columns being processed
            logger.info(f"Categorical columns: {categorical_columns}")
            logger.info(f"Numerical columns: {numerical_columns}")

            # Combining numerical and categorical pipelines into a single ColumnTransformer
            preprocessor = ColumnTransformer(
                transformers=[
                    ("num_pipeline", num_pipeline, numerical_columns),  # Apply numerical pipeline
                    ("cat_pipeline", cat_pipeline, categorical_columns)  # Apply categorical pipeline
                ]
            )

            # Returning the preprocessor object
            return preprocessor

        except Exception as e:
            # Raise a custom exception with context if any error occurs
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path, test_path):
        """
        This method initiates the data transformation process.
        - Reads training and testing datasets
        - Applies the data transformation pipeline
        - Saves the preprocessor object for future use
        - Returns transformed training and testing data along with the preprocessor object path
        """
        try:
            # Reading the training and testing data from CSV files
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logger.info("Read train and test data completed")
            logger.info("Obtaining preprocessing object")

            # Obtain the preprocessor object (pipeline)
            preprocessing_obj = self.get_data_transformer_object()

            # Define the target column and numerical columns
            target_column_name = "math_score"
            numerical_columns = ["writing_score", "reading_score"]

            # Splitting the features and target for training data
            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]

            # Splitting the features and target for testing data
            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            logger.info("Applying preprocessing object on training and testing data")

            # Applying the transformation on training and testing data
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            # Combining the transformed features with the target for training and testing data
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logger.info(f"Saved preprocessing object")

            # Saving the preprocessor object to the specified file path
            save_object(
                file_path=self.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            # Returning the transformed arrays and the preprocessor object path
            return train_arr, test_arr, self.preprocessor_obj_file_path

        except Exception as e:
            # Raise a custom exception with context if any error occurs
            raise CustomException(e, sys)
