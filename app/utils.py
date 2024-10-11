from passlib.context import CryptContext

# bcrypt settings
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password:str):
    return pwd_context.hash(password)


# function to varify the password , db password and user given password

def verify(plain_password , hashed_password):
    return pwd_context.verify(plain_password, hashed_password)