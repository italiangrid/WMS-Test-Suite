class RunCommandError(Exception):
        """Exception raised for errors in the run_command_continue_on_error method

        Attributes:
            expression -- input command in which the error occurred
            message -- explanation of the error
        """

        def __init__(self, expression, message):
            self.expression = expression
            self.message = message

        def __str__(self):
            return repr(self.message)


class GeneralError(Exception):
        """Exception raised for errors ....

        Attributes:
            expression -- input command in which the error occurred
            message -- explanation of the error
        """
        def __init__(self, expression, message):
            self.expression = expression
            self.message = message

        def __str__(self):
            return repr(self.message)


class TimeOutError(Exception):
     
        def __init__(self, expression, message):
            self.expression = expression
            self.message = message

        def __str__(self):
            return repr(self.message)
