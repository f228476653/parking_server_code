import jwt
from .keystore_status_enum import KeystoreStatusEnum
from .keystore_validation_enum import KeystoreValidationEnum
from datetime import datetime,timedelta

class KeystoreManager:
    """ this is not secure at all, however we don't have time to deal this """
    # TODO please re-write entire class to find a better way for generating keys
    
    __jwt_secret = '!@#$%^#$%#!@$!'
    __jwt_algorithm = 'HS256'
    __jwt_exp_delta_seconds = 6000
    def __init__(self
        , start_date:datetime
        , end_Date:datetime
        , fixed_account_total:int
        , dynamic_account_total:int
        , key_manager_email:str
        , service_type:str
        , note:str
        , customer_id:int
        , key_type:str
        , key_status:str
    ):
        # self.__start_date = datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%S.%fZ')
        # self.__end_Date = datetime.strptime(end_Date, '%Y-%m-%dT%H:%M:%S.%fZ')
        self.__start_date = datetime.strptime(start_date[:10], '%Y-%m-%d')
        self.__end_Date = datetime.strptime(end_Date[:10], '%Y-%m-%d')
        self.__fixed_account_total = fixed_account_total
        self.__dynamic_account_total = dynamic_account_total
        self.__key_manager_email = key_manager_email
        self.__service_type = service_type
        self.__note = note
        self.__customer_id = customer_id
        self.__key_type = key_type
        self.__key_status = key_status
        
    def decrypt(self,jwt_token:str):
        """ decrypt with jwt"""
        payload = jwt.decode(jwt_token, self.__jwt_secret, algorithms=[self.__jwt_algorithm])
        return payload

    def verify(self,jwt_token:str) -> KeystoreValidationEnum:
        try:
            result = self.decrypt(jwt_token)
        except jwt.ExpiredSignatureError:
            return KeystoreValidationEnum.EXPIRED
        except jwt.DecodeError:
            return KeystoreValidationEnum.INVALID

        return KeystoreValidationEnum.VALID

    def encrypt(self) -> str:
        """ encrypt with jwt lib"""
        jwt_exp_delta_seconds = self.get_delta_seconds() #cacualte expire total seconds

        payload = {
                '__fixed_account_total': self.__fixed_account_total,
                '__dynamic_account_total':self.__dynamic_account_total,
                '__key_manager_email':self.__key_manager_email,
                '__service_type':self.__service_type,
                '__note':self.__note,
                '__customer_id':self.__customer_id,
                '__key_type':self.__key_type,
                '__key_status':self.__key_status,
                'exp': self.__start_date + timedelta(seconds=jwt_exp_delta_seconds)
        }
        
        encrypted = jwt.encode(payload, self.__jwt_secret, self.__jwt_algorithm)
        return encrypted
        
    def get_delta_seconds(self):
        """ caculate delta seconds for jwt"""
        duration = self.__end_Date - self.__start_date
        duration_in_s = duration.total_seconds()
        return duration_in_s

        
    






