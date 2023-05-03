
class APIClientError(Exception):
    status_code = 400

    def __init__(self, error_msg, status_code=None):
        super().__init__()
        self.error_msg = error_msg
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return {'error': self.error_msg}