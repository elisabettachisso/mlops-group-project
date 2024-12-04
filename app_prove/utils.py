import hashlib

# Funzione per fare hash della password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()