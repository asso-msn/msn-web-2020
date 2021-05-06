class APIError(Exception):
    CODE = 500
    MESSAGE = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.code = kwargs.pop('code', self.CODE)
        self.message = self.MESSAGE

    def __str__(self):
        return 'Error {code}: {text}'.format(
            code=self.code,
            text=self.message or super().__str__(),
        )

class UnauthorizedError(APIError):
    CODE = 401

class ForbiddenError(APIError):
    CODE = 403

class InsufficientPermissionsError(ForbiddenError):
    def __init__(self, *args, role='admin', **kwargs):
        super().__init__(*args, **kwargs)
        self.message = f'You need at least "{role}" permissions to do this'
