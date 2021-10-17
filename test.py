from cryptography.fernet import Fernet

def gen_key():
    key = Fernet.generate_key()
    return key


def encrypt(key, message):
    message = message.encode()
    f = Fernet(key)
    encrypted = f.encrypt(message)
    return encrypted


def decrypt(key, encrypted):
    f = Fernet(key)
    decrypted = f.decrypt(encrypted).decode()
    return decrypted

key = gen_key()
msg = "hi"
e = encrypt(key, msg)
print(e)
d = decrypt(key, e)
print(d)