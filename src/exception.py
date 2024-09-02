import sys
from src.logger import logger  # Import the logger instance from logging_setup

def error_message_detail(error: Exception, error_detail: sys) -> str:
    """
    Generates a detailed error message including file name, line number, and error message.
    
    Args:
    - error (Exception): The exception instance.
    - error_detail (sys): The sys module to extract exception details.

    Returns:
    - str: A formatted error message.
    """
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    error_message = (
        f"Error occurred in file [{file_name}], "
        f"line number [{line_number}]: {str(error)}"
    )
    return error_message

class CustomException(Exception):
    """
    A custom exception class that provides detailed error messages and logs the error.
    
    Inherits from the base Exception class and adds a custom message with traceback information.
    """
    def __init__(self, error: Exception, error_detail: sys):
        """
        Initializes the custom exception with a detailed error message.
        
        Args:
        - error (Exception): The exception instance.
        - error_detail (sys): The sys module to extract exception details.
        """
        # Initialize the base class with the error message
        super().__init__(str(error))
        # Generate and store the detailed error message
        self.error_message = error_message_detail(error, error_detail)
        # Log the error message
        logger.error(self.error_message)

    def __str__(self) -> str:
        """
        Returns the detailed error message.
        
        Returns:
        - str: The detailed error message.
        """
        return self.error_message


"""
if __name__=="__main__":
    try:
        a=1/0
    except Exception as e :
        logger.info("divide by 0 error")
        raise CustomException(e, sys)
"""