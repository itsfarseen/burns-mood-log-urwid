import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet, InvalidToken

class InvalidPassword(Exception):
    pass

class Crypto:
    instance = None

    def __init__(self, password):
        password_provided = password  # This is input in the form of a string
        password = password_provided.encode()  # Convert to type bytes
        salt = b'salt_'  # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))  # Can only use kdf once
        self._key = key
        Crypto.instance = self

    def read_file(self, file):
        f = open(file, 'rb')
        fbytes = f.read()
        f.close()
        if fbytes[0] == 123: # 123 corresponds to open brace
            return fbytes.decode()
        fernet = Fernet(self._key)
        try:
            fbytes_dec = fernet.decrypt(fbytes)
        except InvalidToken:
            raise InvalidPassword()

        fstr = fbytes_dec.decode()
        return fstr

    def write_file(self, file, contents):
        f = open(file, 'wb')
        fbytes = contents.encode()
        fernet = Fernet(self._key)
        fbytes_enc = fernet.encrypt(fbytes)
        f.write(fbytes_enc)
        f.close()
