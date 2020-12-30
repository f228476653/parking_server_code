import aiomysql.sa
from app.config.models import SystemConfiguration, Account
from app.services.service import Service
from app.services.systemlog_service import SystemlogService

class SystemConfigurationService(Service):

    """ 系統參數配置 只有superuser可以使用 新刪修 查詢則無限制"""
    _db = None
    _log_service = None
    _syslog = None
    _user: Account = None
    def __init__(self, db, user: Account):
        self._db = db
        self._log_service = SystemlogService(db)
        self._syslog = {}
        self._user = user
         
    
    async def create_system_configuration(self, data: dict):
        async with self._db.acquire() as conn:
            if self._user.is_superuser:
                result = await conn.execute(SystemConfiguration.insert().values(data))
                return True
            else:
                raise PermissionError("check_account_has_authorization_to_use_system_configuration", "not permit to create system configuration")    

    async def get_all_system_configuration(self):
        async with self._db.acquire() as conn:
            result = [dict(row.items()) for row in await conn.execute(SystemConfiguration.select())]
            return result

    async def get_system_configuration_by_key(self, key: str):
        async with self._db.acquire() as conn:
            result = await conn.execute(SystemConfiguration.select().where(SystemConfiguration.c.key == key))
            result = [dict(row.items()) async for row in result]
            return None if len(result) == 0 else result[0]

    async def get_system_configuration_by_group(self, group: str):
        async with self._db.acquire() as conn:
            #　把該群組資料　組成一個字典回傳
            result = [dict(row.items()) async for row in await conn.execute(SystemConfiguration.select().where(SystemConfiguration.c.config_group_name == group))]
            if len(result) == 0:
                return None
            else:
                data = {}
                for i in result:
                    data[i["key"]] = i["value"]
                return data


    async def delete_system_configuration_by_key(self, key: str):
        async with self._db.acquire() as conn:
            if self._user.is_superuser:
                result = await conn.execute(SystemConfiguration.delete().where(SystemConfiguration.c.key == key))
                return result.rowcount
            else:
                raise PermissionError("check_account_has_authorization_to_use_system_configuration", "not permit to delete system configuration")


    async def update_system_configuration_by_key(self, data: dict):
        async with self._db.acquire() as conn:
            if self._user.is_superuser:
                result = await conn.execute(SystemConfiguration.update().values(data).where(SystemConfiguration.c.key == data['key']))
                return result.rowcount
            else:
                raise PermissionError("check_account_has_authorization_to_use_system_configuration", "not permit to update system configuration")

    
