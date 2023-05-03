import base64
import random
import string


class Random64Token:
    """
    Creates a random base64 token.
    """
    def __init__(self, token_lgth: int = 40):
        self.token = self.generate_token(token_lgth)

    def generate_token(self, token_lgth: int):
        """ Generates a base64 token from a random string with length 'token_lgth'."""
        return self.encode_txt(self.get_random_string(token_lgth))

    @staticmethod
    def get_random_string(lgth: int):
        """ Returns a random string built on ascii characters, with length 'lgth'"""
        random_str = ""
        if lgth > 0:
            while lgth > 0:
                random_str = random_str + random.choice(string.printable.strip())
                lgth -= 1
        else:
            raise ValueError("The random string generated must be 1 or more in length.")
        # print(random_str)
        return random_str

    @staticmethod
    def encode_txt(txt: str) -> str:
        """ Encodes a ascii string 'txt' to a base64 string."""
        message_bytes = txt.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        return base64_bytes.decode('ascii')

    @staticmethod
    def decode_txt64(txt64: str) -> str:
        """ Decodes a base64 string to ascii string."""
        base64_bytes = txt64.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        return message_bytes.decode('ascii')


if __name__ == '__main__':
    token = Random64Token().token
    print(token)
