
import jwt,json
from datetime import datetime, timedelta
from sqlalchemy.sql import select
from app.config.models import Keystore,Garage,Customer,ActivationCode
from sqlalchemy import desc, text
from app.util.encrypt_helper import EncryptHelper
from app.services.exceptions import UserNotExistError,AuthenticationError
from keystore.keystore_manager import KeystoreManager,KeystoreStatusEnum
from keystore.keystore_validation_enum import KeystoreValidationEnum
from keystore.exceptions import KeystoreExpiredError, KeystoreInvalidError
from app.services.systemlog_service import SystemlogService
from app.config.system_event_type import SystemEventType
from app.util.custom_json_encoder import custom_json_handler
import uuid
import string

class KeystoreService:
    """ every thing about key """
    _db =None
    _log_service = None
    _syslog = None
    def __init__(self, db):
        self._db = db
        self._log_service = SystemlogService(db)
        self._syslog = {}

    async def generate_and_save_keystore(self,key:Keystore):
        keystore = await self.generate_encrypted_keystore(key)
        return await self.add_keystore(key)

    async def generate_and_udpate_keystore(self,key:Keystore):
        keystore = await self.generate_encrypted_keystore(key)
        return await self.update_keystore(key,key['keystore_id'])
    
    async def generate_encrypted_keystore(self,key:Keystore)->str:
        keystoreManager = KeystoreManager(
            key['start_date']
            , key['end_date']
            , key['fixed_account_total']
            , key['dynamic_account_total']
            , key['key_manager_email']
            , key['service_type']
            , key['note']
            , key['customer_id']
            , key['key_type']
            , key['key_status'])

        encrypted= keystoreManager.encrypt()

        check_key_status_result = keystoreManager.verify(encrypted)
        key['key_validation_status'] = KeystoreValidationEnum.VALID
        if KeystoreValidationEnum.EXPIRED ==  check_key_status_result:
            raise KeystoreExpiredError('expired')
        elif KeystoreValidationEnum.INVALID == check_key_status_result:
            raise KeystoreInValidError('invalid')
            
        # key['start_date'] = datetime.strptime(key['start_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
        # key['end_date'] = datetime.strptime(key['end_date'], '%Y-%m-%dT%H:%M:%S.%fZ')
        key['start_date'] = datetime.strptime(key['start_date'][:10], '%Y-%m-%d')
        key['end_date'] = datetime.strptime(key['end_date'][:10], '%Y-%m-%d')
        key['key_value'] = encrypted.decode("utf8")
        
        return key

    async def update_keystore_status(self,status:KeystoreStatusEnum, keystore_id:int):
        async with self._db.acquire() as conn:
            result = await conn.execute(Key.update({key_status:Enum(status)}).where(Keystore.c.keystore_id == keystore_id))
            return result.rowcount
        
    async def get_keystores(self):
        """ get keys list """
        async with self._db.acquire() as conn:
            keys = [dict(row.items()) async for row in await conn.execute('select t1.*,t2.company_name from keystore t1 join customer t2 on t1.customer_id = t2.customer_id')]
            return keys

    async def add_keystore(self,key:Keystore):
        self._syslog['create_account_id']=key['create_account_id']
        self._syslog['event_id']=SystemEventType.Add.value
        self._syslog['event_message']=json.dumps(key,default=custom_json_handler)
        #result = await self._log_service.addlog(self._syslog)
        async with self._db.acquire() as conn:
            result = await conn.execute(Keystore.insert(key))
            return result.lastrowid

    async def delete_keystore_by_id(self,keystore_id:int,customer_id:int) -> int:
        self._syslog['create_account_id']=customer_id
        self._syslog['event_id']=SystemEventType.DELETE_INFO.value
        self._syslog['event_message']=json.dumps(keystore_id,default=custom_json_handler)
        #result = await self._log_service.addlog(self._syslog)
        async with self._db.acquire() as conn:
            result = await conn.execute(Keystore.delete().where(Keystore.c.keystore_id == keystore_id))
            return result.rowcount

    async def get_keystores_by_customer_id(self,id:str):
        param = {'id':id}
        sql = """select t1.*,t2.company_name from keystore t1 join customer t2 on t1.customer_id = t2.customer_id where t1.customer_id = :id"""
        async with self._db.acquire() as conn:
            keys = [dict(row.items()) async for row in await conn.execute(text(sql),param)]
            return keys
    
    async def get_keystores_by_id(self,id:int) -> Keystore:
        async with self._db.acquire() as conn:
            data= await conn.execute(Keystore.select().where((Keystore.c.keystore_id == id)))
            return await data.fetchone()
    
    async def update_keystore(self,key,keystore_id:Keystore) -> int:
        self._syslog['create_account_id']=key['create_account_id']
        self._syslog['event_id']=SystemEventType.UPDATE_INFO.value
        self._syslog['event_message']='update_keystore: '+json.dumps(keystore_id,default=custom_json_handler)+json.dumps(key,default=custom_json_handler)
        #result = await self._log_service.addlog(self._syslog)
        async with self._db.acquire() as conn:
            result = await conn.execute(Keystore.update().values(key).where(Keystore.c.keystore_id == keystore_id))
            return result.rowcount

    async def get_pad_config_by_key(self,inital_key) :
        try:
            config = {}
            garage_id = int(inital_key.split('-')[1])
            async with self._db.acquire() as conn :
                customer_id = await conn.execute(select([Garage.c.customer_id]).where(Garage.c.garage_id == garage_id))
                customer_id = await customer_id.scalar()
                r = [dict(row.items()) async for row in await conn.execute(ActivationCode.select().where(ActivationCode.c.garage_id==garage_id).where(ActivationCode.c.activation_code==inital_key))]
                device_key = r[0]['device_key']
                # get device table name
                device_table_sql = """select * from (	select CASE device_type WHEN '3' THEN 'device_pad_args' WHEN '1' THEN 'device_pv3_args' WHEN '4' 
                                THEN 'device_ibox_args' WHEN '2' THEN 'lane' END as device_table
                                from device_view where garage_id =:garage_id and device_key =:device_key) a """
                if len(r) > 0:    
                    garage = [dict(row.items()) async for row in await conn.execute(Garage.select().where(Garage.c.garage_id==garage_id))]
                    customer = [dict(row.items()) async for row in await conn.execute(Customer.select().where(Customer.c.customer_id==customer_id))]
                    device_type = [dict(row.items()) async for row in await conn.execute(text(device_table_sql),{"garage_id" :garage_id ,"device_key" :device_key})]
                    config['garage'] = garage
                    config['customer'] = customer
                    print(device_type)
                    if len(device_type) > 0  and 'device_table' in device_type[0]:
                        device_sql = f"""select * from {device_type[0]['device_table']} where {device_type[0]['device_table']}_id = (select device_id from device_view where garage_id =:garage_id and device_key =:device_key) """
                        device = [dict(row.items()) async for row in await conn.execute(text(device_sql),{"garage_id" :garage_id ,"device_key" :device_key})]
                        config['device'] = device
                else :
                    config['device'] = ''
        except Exception as e:
            print(e)
            config['error'] = 'Server Error'
        return config

    async def encrypt_key_for_pad_config(self,garage_id,device_key,account):
        is_new = await self.check_if_code_created_before(garage_id,device_key)
        async with self._db.acquire() as conn :
            if is_new :
                device_key_after_clear= device_key.replace(".","")
                activation_code = {
                    'activation_code':f"{str(uuid.uuid4())[:4]}-{garage_id}-{device_key_after_clear}",
                    'garage_id':garage_id,
                    'create_account_id':account,
                    'device_key':device_key
                }
                r = await conn.execute (ActivationCode.insert(activation_code))
                return activation_code['activation_code']
            else :
                code = await conn.execute(select([ActivationCode.c.activation_code]).where(ActivationCode.c.garage_id == garage_id).where(ActivationCode.c.device_key == device_key))
                code = await code.scalar()
                return code
    
    async def check_if_code_created_before(self,garage_id,device_key):
        async with self._db.acquire() as conn :
            rs = [dict(row.items()) async for row in await conn.execute(ActivationCode.select()
            .where(ActivationCode.c.garage_id==garage_id)
            .where(ActivationCode.c.device_key==device_key))]
        if len(rs)>0:
            return False
        else:
            return True
                
