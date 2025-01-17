from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated='auto') 

class Hash():

    def bcrypt(password : str):
        return pwd_cxt.hash(password)
    
    def verfiy(hash_password,planed_password):
        return pwd_cxt.verify(planed_password,hash_password)