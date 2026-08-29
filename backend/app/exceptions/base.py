class BaseAppException(Exception):
    error_code = "UNKNOWN_ERROR"
    message = "Something went wrong"
    status_code = 500

    def __init__(self):
        super().__init__(self.message)
