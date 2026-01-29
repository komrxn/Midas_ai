class PaymeException(Exception):
    def __init__(self, code: int, message: dict | str, data: str = None):
        self.code = code
        self.message = message
        self.data = data
