from passlib.hash import pbkdf2_sha256
 
class EncryptHelper(object):

    @staticmethod
    def encrypt(passwd):
        hash = pbkdf2_sha256.encrypt(passwd, rounds=200000, salt_size=16)
        return hash

    @staticmethod
    def verify(first,second):
        return pbkdf2_sha256.verify(first,second)