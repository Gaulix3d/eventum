class WSException(Exception):
    def __init__(self, code, reason):
        # WebSocket status codes range: 1000-1015, 3000-4999
        if not ((1000 <= code <= 1014) or (3000 <= code <= 4999)):
            raise ValueError("Status code must be between 1000-1015 or 3000-4999")
        self.code = code
        self.reason = reason
        super().__init__(f"code: {code}, Message: {reason}")
