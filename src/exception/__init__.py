import sys


def error_message_detail(error: Exception, error_detail=sys) -> str:
    """
    Constructs a detailed error message from an exception, including
    the file name, line number, and exception message.

    Args:
        error (Exception): The caught exception object.
        error_detail (module): Typically the `sys` module to access exc_info.

    Returns:
        str: Formatted error message with traceback info.
    """
    exc_type, exc_obj, exc_tb = error_detail.exc_info()

    if exc_tb is not None:
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno
        error_msg = (
            f"Error occurred in script [{file_name}] at line [{line_number}] "
            f"with message: {str(error)}"
        )
    else:
        error_msg = str(error)

    return error_msg


class AppException(Exception):
    """
    Custom exception class that adds file name and line number
    context to the original exception.

    Attributes:
        error_message (str): Detailed error description.
    """

    def __init__(self, error: Exception, error_detail=sys):
        """
        Initializes the AppException with a detailed message.

        Args:
            error (Exception): The original exception.
            error_detail: Typically the `sys` module (default is `sys`).
        """
        super().__init__(str(error))
        self.error_message = error_message_detail(error, error_detail)

    def __str__(self) -> str:
        return self.error_message