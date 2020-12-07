class SignatureError(Exception):
    def __init__(self, payload=None, status_code=400,):
        Exception.__init__(self)
        self.payload = payload
        self.status_code = status_code

    def to_dict(self):
        return dict(self.payload or ())
