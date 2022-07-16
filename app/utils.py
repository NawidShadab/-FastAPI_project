# this content some utils functions

from passlib.context import CryptContext

# our hashing algorithm for passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# method for hashing passwords
def hash(password: str):
    return pwd_context.hash(password)


# comparing the hashed passwords from db and what client gives if they are the same
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
 
    