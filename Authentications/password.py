import bcrypt

def hash_pass(password: str) -> str:
    pass_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(pass_bytes, salt)
    return hashed.decode("utf-8")

def verify_pass(plain_pass:str, hashed_pass:str)->bool:
    return bcrypt.checkpw(plain_pass.encode("utf-8"), hashed_pass.encode("utf-8"))