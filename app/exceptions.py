class APIError(Exception):
    CODE = 500

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.code = kwargs.pop('code', self.CODE)

    def __str__(self):
        return 'Error {code}: {text}'.format(
            code=self.code,
            text=super().__str__(),
        )
