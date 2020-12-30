from aiohttp.web import Request,Application
import time
import jwt,json
from datetime import datetime, timedelta
from sqlalchemy import desc,text
from sqlalchemy.orm import Session,sessionmaker
from app.config.models import Account,Role,Permission,Map_Role_Permission,SystemLog, ForgetPassword ,Map_Garage_To_Account, Map_Garage_Group_To_Account
from app.services.service import Service
from app.util.encrypt_helper import EncryptHelper
from app.services.exceptions import UserNotExistError,AuthenticationError,ExistError, DuplicateError
from app.custom_errors.permission_error import PermissionError

from app.util.custom_json_encoder import custom_json_handler
from app.services.systemlog_service import SystemlogService
from app.services.customer_service import CustomerService
from app.config.system_event_type import SystemEventType
from pprint import pprint

class UserService(Service):
    """ every thing about user , like account, permission, role"""
    _db = None
    _log_service = None
    _syslog = None
    _user: Account = None
    def __init__(self, db, user: Account):
        self._db = db
        self._user =user
        self._log_service = SystemlogService(self._db)
        self._syslog = {}
        
    async def get_permissions(self):
        """ get all permissions """
        async with self._db.acquire() as conn:
            permission = [dict(row.items()) async for row in await conn.execute(Permission.select().order_by(Permission.c.permission_id))]
            return permission
        
    async def get_permission_by_id(self,id):
        """ get permission by id """
        async with self._db.acquire() as conn:
            result= await conn.execute(Permission.select().where((Permission.c.permission_id == id)))
            permission= await result.fetchone()
            if permission is not None:
                return permission
            else:
                return None

    async def get_permissions_by_role_id(self,role_id):
        """ get permission by id """
        async with self._db.acquire() as conn:
            roles = [dict(row.items()) async for row in await conn.execute(Map_Role_Permission.select().where(Map_Role_Permission.c.role_id == role_id))]
            return roles

    async def get_maximun_permission(self):
        async with self._db.acquire() as conn:
            condition = {
                'customer_id':self._user.customer_id
            }
            sql = """ select c.* from role a join map_role_permission b on a.role_id = b.role_id
                join permission c on b.permission_id = c.permission_id 
                where a.customer_id =:customer_id and a.is_system_role = 1 """
            result = [dict(row.items()) async for row in await conn.execute(text(sql),condition)]
            return result

    async def get_customer_maximun_permission(self):
        async with self._db.acquire() as conn:
            condition = {
                'customer_id':self._user.customer_id
            }
            sql = """ select c.* from role a
                join map_role_permission b on a.role_id = b.role_id
                join permission c on b.permission_id = c.permission_id 
                where a.role_id = (select role_id from account where customer_id =:customer_id and is_customer_root = 1)
            """
            result = [dict(row.items()) async for row in await conn.execute(text(sql),condition)]
            return result

    async def has_permission(self,role_id:int, permission_id:int) -> bool:
        return True;

    async def get_roles(self):
        print(f'---role--{self._user}')
        async with self._db.acquire() as conn:
            if self._user.is_superuser:
                roles = [dict(row.items()) async for row in await conn.execute(Role.select().order_by(desc(Role.c.create_date)))]
            else:
                roles = await self.get_roles_by_customer_id(self._user.customer_id)
            return roles


    async def get_roles_by_customer_id(self,customer_id):
        async with self._db.acquire() as conn:
            condition = {
                    'customer_id':customer_id
            }
            sql = """select a.*,b.company_name from role a join customer b on a.customer_id = b.customer_id 
                    where a.customer_id=:customer_id order by create_date desc"""
            roles = [dict(row.items()) async for row in await conn.execute(text(sql),condition)]
            return roles

    async def get_role_by_id(self,id):
        async with self._db.acquire() as conn:
            roles = [dict(row.items()) async for row in await conn.execute(Role.select().where(Role.c.role_id == id))]
            return roles

    async def is_role_name_exist_by_customer_id(self,role_name: str) -> bool:
        async with self._db.acquire() as conn:
            sql = """ select * from role where name =:role_name"""
            condition = {
                "role_name": role_name
            }
            print(sql)
            result = [dict(row.items()) async for row in await conn.execute(text(sql),condition)]
            return len(result) >0 and True or False

    async def add_role(self,role,permission:[Permission]):
        self._syslog['create_account_id']=role['create_account_id']
        self._syslog['event_id']=SystemEventType.ADD_ROLE.value
        self._syslog['event_message']= json.dumps(role,default=custom_json_handler)+json.dumps(permission,default=custom_json_handler)
        result = await self._log_service.addlog(self._syslog)
        if await self.is_role_name_exist_by_customer_id(role['name']):
            raise ExistError('role name exist')

        async with self._db.acquire() as conn:
            result = await conn.execute(Role.insert().values(role))
            print(role)
            print('-----------')
            k = await conn.execute('SELECT LAST_INSERT_ID() AS id')
            resultone = await k.fetchone()
            kk = resultone.get(0)
            await conn.execute(Map_Role_Permission.delete().where((Map_Role_Permission.c.role_id==kk)))
            for item in permission:
                await conn.execute(Map_Role_Permission.insert().values(permission_id = item['permission_id'],role_id=kk))
            return kk

    async def update_role(self,role,permission:[Permission]):
        self._syslog['create_account_id']=role['create_account_id']
        self._syslog['event_id']=SystemEventType.UPDATE_INFO.value
        self._syslog['event_message']= 'update_role: '+json.dumps(role,default=custom_json_handler)+json.dumps(permission,default=custom_json_handler)
        #result = await self._log_service.addlog(self._syslog)
        async with self._db.acquire() as conn:
            result = await conn.execute(Role.update().values(role).where(Role.c.role_id == role['role_id']))
            await conn.execute(Map_Role_Permission.delete().where((Map_Role_Permission.c.role_id==role['role_id'])))
            for item in permission:
                await conn.execute(Map_Role_Permission.insert().values(permission_id = item['permission_id'],role_id=role['role_id']))
            return role['role_id']

    async def delete_role(self,role_id,account_id) -> bool:
        self._syslog['create_account_id']=account_id
        self._syslog['event_id']=SystemEventType.DELETE_INFO.value
        self._syslog['event_message']= 'delete_role: '+json.dumps(role_id,default=custom_json_handler)
        #result = await self._log_service.addlog(self._syslog)
        async with self._db.acquire() as conn:
            result = await conn.execute(Account.select().where((Account.c.role_id == role_id)))
            one = await result.fetchone()
            if one is None and role_id !='1':
                await conn.execute(Role.delete().where(Role.c.role_id==role_id))
                await conn.execute(Map_Role_Permission.delete().where((Map_Role_Permission.c.role_id==role_id)))
                return True
            else:
                return False

    async def login(self,account,password,jwt_exp_delta_seconds,jwt_secret,jwt_algorithm):
        """ try login and get token string """
        user =  await self.get_first_by_account(account)
        if user is None:
            raise UserNotExistError(account)
        customer_service = CustomerService(self._db,user)
        customer = await customer_service.get_customer_by_id(user.customer_id)
        if customer is None:
            raise AuthenticationError('customer is not exist')
        
        if customer['customer_status'] == 0:
            raise AuthenticationError('customer is inactive')

        if EncryptHelper.verify(password,user.password):
            
            payload = {
                'id': user.account_id,
                'test':'test',
                'exp': datetime.utcnow() + timedelta(seconds=jwt_exp_delta_seconds)
            }
            return {
            'account_id':user.account_id
            ,'is_superuser':user.is_superuser
            ,'token': jwt.encode(payload, jwt_secret, jwt_algorithm)
            ,'user_name':("{}{}".format((user.user_first_name or ""),(user.user_last_name or "")))
            ,'account':user.account
            ,'customer_id':user.customer_id
            ,'role_id':user.role_id
            ,'is_customer_root':user.is_customer_root
            ,'is_api_user':user.is_api_user
        }
        else:
            raise AuthenticationError(account)

    async def forget_passward_query_reset(self ,email,jwt_secret,jwt_algorithm,jwt_exp_delta_seconds):
        print("forget_passward_query_reset")
        async with self._db.acquire() as conn:
            accounts = [dict(row.items()) async for row in await conn.execute(
                    Account.select().where((Account.c.email == email)))]
            if len(accounts) >1 :
                return FoundMultipleError('Email has been enroll to over two accounts')
            if len(accounts) == 0 :
                return ExistError('Email has been enroll to over two accounts')
            else:
                forget_password = {}
                forget_password['email'] = email
                forget_password['account_id'] = accounts[0]['account_id']
                forget_password['account'] = accounts[0]['account']
                payload = {
                    'id': accounts[0]['account_id'],
                    'test':'test',
                    'exp': datetime.utcnow() + timedelta(seconds=jwt_exp_delta_seconds)
                }
                forget_password['token'] = jwt.encode(payload, jwt_secret, jwt_algorithm)
                print(f"-----token----{forget_password['token']}")
                r = await conn.execute(ForgetPassword.insert().values(forget_password))
                print(f"-token_after---{str(forget_password['token'])}")
                subject = 'Reset PMS+ Password'
                msgText =f""" Please click the URL blow to reset passwaord \n http://localhost:4200/login/reset-password/{str(forget_password['token'])}"""
                if r.lastrowid is not None :
                    emailservice = EmailService()
                    to_mail = []
                    to_mail.append(forget_password['email'])
                    emailservice.send_pure_email( to_mail , forget_password['account'] ,msgText ,subject)
                return True
    
    async def get_reset_password_account(self,token):
        now = datetime.utcnow()
        async with self._db.acquire() as conn:
            #forgetPwd = [dict(row.items()) async for row in await conn.execute(ForgetPassword.select().order_by(desc(ForgetPassword.c.expiration_date)))]
            forgetPwd = [dict(row.items()) async for row in await conn.execute(ForgetPassword.select().where(ForgetPassword.c.token == token).order_by(desc(ForgetPassword.c.expiration_date)))]
            print(f'--forgetPwd--{forgetPwd}')
            if len(forgetPwd) > 0:
                now = int(time.time())
                expiration_date = time.mktime(forgetPwd[0]['expiration_date'].timetuple())
                print(f'--now--{now>expiration_date}')
                if now > expiration_date:
                    account ={'account' :'' , 'account_id' : ''}
                    return account
                else:
                    account = [dict(row.items()) async for row in await conn.execute(Account.select().where(Account.c.account_id == forgetPwd[0]['account_id'] ))]
                    print(account)
                    return account[0]
            else :
                account ={'account' :'' , 'account_id' : ''}
                return account

    async def update_password(self,account):
        async with self._db.acquire() as conn:
            trans =await conn.begin() 
            try: 
                result = await conn.execute(Account.update().values(account).where(Account.c.account_id == account['account_id']))
                self._syslog['create_account_id']=account['account_id']
                self._syslog['event_id']=SystemEventType.UPDATE_INFO.value
                self._syslog['event_message']= 'update_user: '+json.dumps(account,default=custom_json_handler)
                result = await self._log_service.addlog(self._syslog)
            except Exception as e:
                await trans.rollback()
                raise
            else:
                await trans.commit()
                return True

        
    async def get_users(self):
        """ get all users """
        async with self._db.acquire() as conn:
            if self._user.is_superuser:
                accounts = [dict(row.items()) async for row in await conn.execute("SELECT a.* ,UNIX_TIMESTAMP(a.modified_date) AS modified_date_unix,UNIX_TIMESTAMP(a.create_date) AS create_date_unix, c.company_name FROM account AS a LEFT JOIN customer AS c ON a.customer_id = c.customer_id ORDER by a.account_id")]
            elif self._user.is_customer_root:
                sql = "SELECT a.* ,UNIX_TIMESTAMP(a.modified_date) AS modified_date_unix,UNIX_TIMESTAMP(a.create_date) AS create_date_unix, c.company_name FROM account AS a LEFT JOIN customer AS c ON a.customer_id = c.customer_id WHERE a.customer_id =:customer_id order by a.create_date desc"
                condition = {
                    "customer_id":self._user.customer_id
                }
                accounts = [dict(row.items()) async for row in await conn.execute(text(sql),condition)]
            else :
                sql = f"""SELECT a.* ,UNIX_TIMESTAMP(a.modified_date) AS modified_date_unix,UNIX_TIMESTAMP(a.create_date) AS create_date_unix
                , c.company_name FROM account AS a LEFT JOIN customer AS c ON a.customer_id = c.customer_id WHERE a.customer_id =:customer_id 
                and a.account_id =:account_id order by a.create_date desc"""
                condition = {
                    "customer_id":self._user.customer_id,
                    "account_id":self._user.account_id
                }
                accounts = [dict(row.items()) async for row in await conn.execute(text(sql),condition)]
            return accounts

    async def is_account_exist(self,account):
        """ to check an account is exist or not """
        async with self._db.acquire() as conn:
            accounts= [dict(row.items()) async for row in await conn.execute(
                    Account.select().where((Account.c.account == account)))
                ]
            return len(accounts) >0 and True or False

    async def get_users_by_customer_id(self,customer_id):
        """ get account by customer_id """
        async with self._db.acquire() as conn:
            condition = {
                'customer_id' : customer_id
            }
            sql = "select * ,UNIX_TIMESTAMP(modified_date) as modified_date_unix,UNIX_TIMESTAMP(create_date) as create_date_unix from account where customer_id = :customer_id and is_superuser = 0"
            result = [dict(row.items()) async for row in await conn.execute(text(sql),condition)]
            return result
    
    async def get_users_by_customer_id_with_system_account(self,customer_id):
        """ get account by customer_id """
        async with self._db.acquire() as conn:
            condition = {
                'customer_id' : customer_id
            }
            sql = "select * ,UNIX_TIMESTAMP(modified_date) as modified_date_unix,UNIX_TIMESTAMP(create_date) as create_date_unix from account where customer_id = :customer_id or customer_id = 0"
            result = [dict(row.items()) async for row in await conn.execute(text(sql),condition)]
            return result

    async def is_account_exist(self, account: str):
        async with self._db.acquire() as conn:
            condition = {
                'account' : account
            }
            sql = "select * ,UNIX_TIMESTAMP(modified_date) as modified_date_unix,UNIX_TIMESTAMP(create_date) as create_date_unix from account where account =:account"
            accounts= [dict(row.items()) async for row in await conn.execute(text(sql),condition)]
            return accounts
    
    async def get_user_by_account(self, account: str):
        if not self._user.is_superuser and not self.is_account_in_has_same_customer_id(self._user.account, account):
            raise PermissionError('is_account_in_has_same_customer_id',"not permit to quesry other customer's data" )
        
        async with self._db.acquire() as conn:
            condition = {
                'account' : account
            }
            sql = "select * ,UNIX_TIMESTAMP(modified_date) as modified_date_unix,UNIX_TIMESTAMP(create_date) as create_date_unix from account where account =:account"
            accounts= [dict(row.items()) async for row in await conn.execute(text(sql),condition)]
            return accounts

    async def get_user_by_account_id(self,id):
        """ get account by account_id """
        async with self._db.acquire() as conn:
            condition = {
                'id' : id
            }
            sql = "select * ,UNIX_TIMESTAMP(modified_date) as modified_date_unix,UNIX_TIMESTAMP(create_date) as create_date_unix from account where account_id =:id"
            accounts= [dict(row.items()) async for row in await conn.execute(text(sql),condition)]
            return accounts

    async def get_account_latest_update_date_by_garage_id(self,garage_id: int, order= 'b.modified_date', desc='desc') -> str:
        result = await self.get_users_by_garage_id(garage_id,order,desc)
        modified_date= []
        for r in range(len(result)):
            modified_date.append(result[r]['modified_date'])
        sort_modified_date = sorted(modified_date,reverse = True)
        return len(sort_modified_date) > 0 and str(sort_modified_date[0]) or '1980-01-01 00:00:00'
    
    async def get_users_by_garage_id_xor_customer_id(self,garage_id: int) -> [Account]:
        """ get user's garage list """
        if not self._user.is_superuser:
            return await self.get_users_by_garage_id_and_customer_id(self._user.customer_id, garage_id)
        else:
            return await self.get_users_by_garage_id(garage_id)
    
    async def get_users_by_garage_id(self,garage_id: int, order='b.account',desc='desc') -> [Account]:
        async with self._db.acquire() as conn:
                sql = """ select c.*,UNIX_TIMESTAMP(c.modified_date) as modified_date_unix,UNIX_TIMESTAMP(c.create_date) as create_date_unix  from map_garage_to_garage_group a join map_garage_group_to_account b on a.garage_group_id = b.garage_group_id join account c on b.account_id=c.account_id
where a.garage_id =:garage_id
                order by :order :desc"""
                condition = {
                    "garage_id": garage_id,
                    "order": order,
                    "desc": desc
                }
                accounts = [dict(row.items()) async for row in await conn.execute(text(sql),condition)]
                return accounts

    async def get_users_by_garage_id_and_customer_id(self, customer_id: int ,garage_id: int, order='b.account',desc='desc') -> [Account]:
        async with self._db.acquire() as conn:
                sql ="""
                select c.*,UNIX_TIMESTAMP(c.modified_date) as modified_date_unix,UNIX_TIMESTAMP(c.create_date) as create_date_unix  from map_garage_to_garage_group a join map_garage_group_to_account b on a.garage_group_id = b.garage_group_id join account c on b.account_id=c.account_id
where a.garage_id =:garage_id and c.customer_id=:customer_id
                order by :order :desc """
                condition = {
                    "garage_id": garage_id,
                    "customer_id": self._user.customer_id,
                    "order":order,
                    "desc":desc
                }
                accounts = [dict(row.items()) async for row in await conn.execute(text(sql),condition)]
                return accounts

    async def get_first_by_account_id(self,id):
        """ get one account by account_id """
        async with self._db.acquire() as conn:
            result= await conn.execute(Account.select().where((Account.c.account_id == id)))
            acc= await result.fetchone()
            return acc
    
    async def get_first_by_account(self,account):
        """ get account by account """
        async with self._db.acquire() as conn:
            result= await conn.execute(Account.select().where((Account.c.account == account)))
            acc= await result.fetchone()
            return acc

    async def delete_user_by_id(self,account_id,login_id):
        self._syslog['create_account_id']=login_id
        self._syslog['event_id']=SystemEventType.DELETE_INFO.value
        self._syslog['event_message']= 'delete_user_by_id: account_id = '+account_id
        #result = await self._log_service.addlog(self._syslog)

        id = int(account_id)
        async with self._db.acquire() as conn:
            result = await conn.execute(Account.delete().where(Account.c.account_id == id))
            return result.rowcount



    async def get_map_garage_to_account_list_by_acocunt_id(self, account_id: int) -> [int]:
        if self._user.is_superuser or await self.is_account_id_in_has_same_customer_id(self._user.customer_id,account_id):
            async with self._db.acquire() as conn:
                sql = """ select garage_id from map_garage_to_account where account_id =:account_id 
                    union all
                    select c.garage_id from map_garage_group_to_account a join garage_group b on a.garage_group_id = b.garage_group_id
                join map_garage_to_garage_group c on b.garage_group_id = c.garage_group_id 
                where a.account_id=:account_id
                """
                condition = {
                    "account_id": account_id
                }
                accounts = [dict(row.items()) async for row in await conn.execute(text(sql),condition)]
                return accounts
        else:
            raise PermissionError("is_account_id_in_has_same_customer_id","not permit to quesry other customer's data")

    async def get_map_garage_to_account_by_account_id(self,account_id:int):
        """ get user's garage list """
        if self._user.is_superuser or await self.is_account_id_in_has_same_customer_id(self._user.customer_id,account_id):
            async with self._db.acquire() as conn:
                sql = """ select * from map_garage_to_account where account_id =:account_id """
                condition = {
                    "account_id": account_id
                }
                accounts = [dict(row.items()) async for row in await conn.execute(text(sql),condition)]
                return accounts
        else:
            raise PermissionError("is_account_id_in_has_same_customer_id","not permit to quesry other customer's data")

    async def get_map_garage_group_to_account_by_account_id(self, account_id):
        """ get user's garage list """
        if self._user.is_superuser or await self.is_account_id_in_has_same_customer_id(self._user.customer_id,account_id):
            async with self._db.acquire() as conn:
                sql = """select c.* from map_garage_group_to_account a join garage_group b on a.garage_group_id = b.garage_group_id
                join map_garage_to_garage_group c on b.garage_group_id = c.garage_group_id 
                where a.account_id=:account_id """

                condition = { 
                    "account_id": self._user.account_id
                }
                result = [dict(row.items()) async for row in await conn.execute(text(sql), condition)]
                return result
        else:
            raise PermissionError("is_account_id_in_has_same_customer_id","not permit to quesry other customer's data")
            


            
