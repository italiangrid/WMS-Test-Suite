class RunCommandError(Exception):

        """Exception raised for errors in the run_command_continue_on_error method

        Attributes:
            expression -- input command in which the error occurred
            message -- error explanation and details
        """

        def __init__(self, expression, message):
            self.expression = expression
            self.message = message

        def __str__(self):
            return repr(self.message)


class GeneralError(Exception):

        """Exception raised for general errors in various operations and methods

        Attributes:
            expression -- operation or method where the error occurred
            message -- error explanation and details
        """

        def __init__(self, expression, message):
            self.expression = expression
            self.message = message

        def __str__(self):
            return repr(self.message)


class TimeOutError(Exception):

        """Exception raised when maximum number of retries has been reached

        Attributes:
            expression -- operation or method where the error occurred
            message -- error explanation and details
        """
     
        def __init__(self, expression, message):
            self.expression = expression
            self.message = message

        def __str__(self):
            return repr(self.message)

