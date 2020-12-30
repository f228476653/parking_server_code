class ApiResponse:
    error: dict = None

    def __init__(self, data, has_error: bool = False, message: str = 'success', error: 'ApiResponse.Error'=None):
        self.data = data
        self.has_error = has_error
        self.message = message

        # for compatible with the error response format
        if error is None:
            import app.custom_errors.api_error_data as api_error_data
            self.error = api_error_data.ApiErrorGeneric.UnexpectedError(message).api_error().asdict() if has_error is True else None
        else:
            self.error = error.asdict()
            self.has_error = True
            self.message = error.title

    def asdict(self):
        return self.__dict__

    class Error:
        def __init__(self, code: str, title: str, detail: str):
            self.code = code
            self.title = title
            self.detail = detail

        def asdict(self):
            return self.__dict__

