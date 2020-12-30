"""Application module."""
import os, time
from app.config.settings import Settings
from app.config.routes import map_routes
from aiomysql.sa import create_engine
from sqlalchemy import text
from app.util.encrypt_helper import EncryptHelper
from app.config.models import Account,Customer,Role,Map_Role_Permission,Permission, Garage
from app.config.models import Map_Garage_To_Garage_Group,GarageGroup,Map_Garage_To_Account
from app.config.models import SystemConfiguration
from app.config.db_version_control import DBVersionControl
from datetime import datetime
import asyncio

environment_settings = None

async def startup(app):
    """Startup app. set jwt config here because we don't want jwt is configurable"""
    app['jwt_secret'] = 'secret'  # note! Changing JWT configuration will fail authorization 
    app['jwt_algorithm'] = 'HS256'
    app['jwt_exp_delta_seconds'] = 60000000
    app['jwt_exp_delta_seconds_remember_me'] = 36000000
    app.logger.info('starting up server')

async def cleanup(app): 
    """Cleanup app."""
    # Mysql/MariaDB
    app.logger.info('server shutdown')
    app['pmsdb'].close()
    await app['pmsdb'].wait_closed()
    app['pmsdb'] = None



async def attach_db(app):
    app.logger.info("mysql host:{}, port: {}, dbname: {}, username: {}, pass: {}".format(
        environment_settings.SETTINGS['mysql']['host']
        ,environment_settings.SETTINGS['mysql']['port']
        ,environment_settings.SETTINGS['mysql']['dbname']
        ,environment_settings.SETTINGS['mysql']['username']
        ,environment_settings.SETTINGS['mysql']['passwd'])
    )
    app['pmsdb'] = await create_engine(
            host=environment_settings.SETTINGS['mysql']['host'],
            port=int(environment_settings.SETTINGS['mysql']['port']),
            db=environment_settings.SETTINGS['mysql']['dbname'],
            user=environment_settings.SETTINGS['mysql']['username'],
            password=environment_settings.SETTINGS['mysql']['passwd'],
            autocommit=environment_settings.SETTINGS['mysql']['autocommit'],
            echo=False,
            charset='utf8',
            use_unicode=True,
            sql_mode='NO_AUTO_VALUE_ON_ZERO',
            maxsize=1000
    )
    print(f"------{environment_settings.SETTINGS['mysql']}")

async def populate_init_values(engine):
    """generate default data to database."""

    root_passwd = EncryptHelper().encrypt('123')
    user_passwd = EncryptHelper().encrypt('123')
    await populate_permission(engine)
    async with engine.acquire() as conn:
        await conn.execute(Account.insert().values({'account': 'system', 'is_customer_root':0 ,'password': root_passwd,'is_api_user': False ,'is_superuser':True,'role_id':1,'create_account_id':1,'customer_id':0}))
        await conn.execute(Account.insert().values({'account': 'root', 'is_customer_root':0 ,'password': root_passwd,'is_api_user': False,'is_superuser':True,'role_id':1,'create_account_id':1,'customer_id':0}))
        await conn.execute(Customer.insert().values({'customer_id':0, 'customer_code':'8001','company_union_number':'800101','contact_username': 'root', 'company_name': u'Acer ITS','customer_status':1,'phone_number1':'02-26963690#8301','create_account_id':0}))
        """ 新增系統用戶管理員預設權限 """
        await conn.execute(Role.insert().values({'role_id':1, 'name': 'root_admin', 'description': 'root admin role','role_type':'root_admin','is_system_role':1,'customer_id':0,'create_account_id':0}))
        pad_permission = getAllAdminPermission()
        for w in pad_permission:
            await conn.execute(Map_Role_Permission.insert().values({'role_id': 1, 'permission_id': w, 'create_account_id':0}))
        
        """新增平板型用戶管理員預設角色與權限  """
        await conn.execute(Role.insert().values({'role_id':2, 'name': 'pad_admin', 'description': 'admin role','role_type':'pad_admin','is_system_role':1,'customer_id':1,'create_account_id':0}))
        pad_permission = getPadAdminPermission()
        for w in pad_permission:
            await conn.execute(Map_Role_Permission.insert().values({'role_id': 2, 'permission_id': w, 'create_account_id':0}))

    
        
def getPadAdminPermission():
    """ 取得平板型用戶 權限 """
    return [1,2,3,4,5,6,11,12,13,31,32,33,91,92,93,111,112,113,131,143,181,182]

def getAllAdminPermission():
    """ 取得最大 權限 """
    return [1,2,3,4,5,6,11,12,13,21,22,23,191,192,193,31,32,33,41,42,43,51,52,53,54,61,62,63,65,64,66,67,71,72,73,74,75,81,82,83,91,92,93,111,112,113,121,122,123,131,132,133,141,142,143,144,151,152,153,154,161,162,163,163,181,182,183]

async def populate_permission(engine):
    
    """ 維運管理群組 """
    async with engine.acquire() as conn:
        """ 1,2, 11, 21, 31, 91, 101,111,121,131,132,151,152,153,154,181,182"""
        await conn.execute(Permission.insert().values({'permission_id':1,'name': '維運管理', 'description': '維運管理功能群組','permission_type':'group','create_account_id':0,'parent_id':0}))

        await conn.execute(Permission.insert().values({'permission_id':2,'name': '帳號管理', 'description': '帳號管理功能','permission_type':'page','create_account_id':0,'parent_id':1}))
        await conn.execute(Permission.insert().values({'permission_id':3,'name': '帳號修改', 'description': '帳號管理修改功能','permission_type':'page_feature','create_account_id':0,'parent_id':2}))
        await conn.execute(Permission.insert().values({'permission_id':4,'name': '帳號刪除', 'description': '帳號管理刪除功能ˊ','permission_type':'page_feature','create_account_id':0,'parent_id':2}))
        await conn.execute(Permission.insert().values({'permission_id':5,'name': '帳號場站指派', 'description': '帳號管理場站指派','permission_type':'page_feature','create_account_id':0,'parent_id':2}))
        await conn.execute(Permission.insert().values({'permission_id':6,'name': '帳號角色指派', 'description': '帳號管理角色指派', 'permission_type':'page_feature','create_account_id':0,'parent_id':2}))

        await conn.execute(Permission.insert().values({'permission_id':11,'name': '角色管理', 'description': '角色管理功能','permission_type':'page','create_account_id':0,'parent_id':0}))
        await conn.execute(Permission.insert().values({'permission_id':12,'name': '角色修改', 'description': '角色管理修改功能','permission_type':'page_feature','create_account_id':0,'parent_id':11}))
        await conn.execute(Permission.insert().values({'permission_id':13,'name': '角色刪除', 'description': '角色管理刪除功能ˊ','permission_type':'page_feature','create_account_id':0,'parent_id':11}))

        await conn.execute(Permission.insert().values({'permission_id':21,'name': '客戶管理', 'description': '客戶管理功能','permission_type':'page','create_account_id':0,'parent_id':0}))
        await conn.execute(Permission.insert().values({'permission_id':22,'name': '客戶基本設定修改', 'description': '客戶管理修改功能','permission_type':'page_feature','create_account_id':0,'parent_id':21}))
        await conn.execute(Permission.insert().values({'permission_id':23,'name': '客戶刪除', 'description': '客戶管理刪除功能ˊ','permission_type':'page_feature','create_account_id':0,'parent_id':21}))

        await conn.execute(Permission.insert().values({'permission_id':191,'name': '客戶行事曆匯入', 'description': '客戶行事曆匯入','permission_type':'page_feature','create_account_id':0,'parent_id':21}))
        await conn.execute(Permission.insert().values({'permission_id':192,'name': '客戶行事曆匯出', 'description': '客戶行事曆匯出','permission_type':'page_feature','create_account_id':0,'parent_id':21}))
        await conn.execute(Permission.insert().values({'permission_id':193,'name': '客戶行事曆產出dat', 'description': '客戶行事曆產出dat','permission_type':'page_feature','create_account_id':0,'parent_id':21}))

        await conn.execute(Permission.insert().values({'permission_id':31,'name': '場站管理', 'description': '場站管理功能','permission_type':'page','create_account_id':0,'parent_id':0}))
        await conn.execute(Permission.insert().values({'permission_id':32,'name': '場站基本設定修改', 'description': '場站管理修改功能','permission_type':'page_feature','create_account_id':0,'parent_id':31}))
        await conn.execute(Permission.insert().values({'permission_id':33,'name': '場站刪除', 'description': '場站管理刪除功能ˊ','permission_type':'page_feature','create_account_id':0,'parent_id':31}))

 
async def update_schema(engine, update_schema_list: list):
    """update"""
    root_passwd = EncryptHelper().encrypt('@@123qwe')
    user_passwd = EncryptHelper().encrypt('123')
    async with engine.acquire() as conn:
        for sql in update_schema_list:
            print(sql)
            c = [dict(row.items()) async for row in await conn.execute(text(sql),{'customer_id' : 2})]
            #c = await conn.execute(text(sql))
            # d = [dict(i.items() async for i in c)]
            print(c)
    print('update finished')

async def read_prodcution_env(app):
    await environment_settings.load_environment()

async def read_custom_env(app):
    await environment_settings.load_environment(app['command_args'].env)

async def read_develop_env(app):
    await environment_settings.load_environment()
    print (environment_settings.SETTINGS)

async def fast_enable_kevin_env(app):
    await environment_settings.load_environment(app['command_args'].p)    
    
async def handle_db_schema(app):
    db_version_clause =  app['command_args'].db
    schema = DBVersionControl(app['pmsdb'])
    status = db_version_clause[0]
    # try:
    if status == "init":
        await schema.V0_0()
        result = {"is_corrent": True, "index_start" : 0, "index_end": len(schema.version) -1}
    elif status == "update":
        version_number = show_db_version()
        if version_number == db_version_clause[1]:
            result = schema.is_correct_version_number(float(db_version_clause[1]), float(db_version_clause[2]))
        else:
            message = '''current version no match please checkout version.txt
            current version:{0}
            input current version:{1}
            '''.format(version_number, db_version_clause[1])
            raise Exception(message)
    elif status == "backup":
        # TODO backup db sql
        print("start backup")
        await schema.back()
    else:
        print('prefix no match')
        return
    if result['is_corrent']:
        for i in schema.version[result['index_start'] : result['index_end'] + 1]:
            version_no = "v" + str(i).replace('.', '_')
            update_schema = getattr(schema, version_no)
            await update_schema()
        if status == "init":
            await populate_init_values(app['pmsdb'])
        # write schema version to version.txt
        update_version_index = result['index_end']
        version = "v" + str(schema.version[update_version_index])
        with open("./version.txt", "w+") as f:
            version_message = "db schema version : " + version
            print('目前版本:', version_message)
            f.write(version_message)
        f.close()
    else:
        print('輸入版本號有誤 請確認有此版本', result['version_start'], result['version_end'])
    # except Exception as e:
    #     print('更新DB版本出現錯誤 ', e)
        

def show_db_version():
    if os.path.isfile("./version.txt"):
        with open("./version.txt", "r") as f:
            r = f.readlines()
            result = r[-1]
        f.close()
        print(result)
        version = result.split(': v')
        version_number = version[1].rsplit()
        return version_number[0]
    else:
        version_number = '查無檔案version.txt'
        print(version_number)
        return version_number

def app_config(app):
    global environment_settings
    environment_settings = Settings()
    """Add app configs."""
    if app['command_args'].prod:
        app.on_startup.append(read_prodcution_env)
    # elif app['command_args'].p:
    #     app.on_startup.append(fast_enable_kevin_env)
    elif app['command_args'].env:
        app.on_startup.append(read_custom_env)
    else:
        app.on_startup.append(read_develop_env)
    
    #app.on_startup.append(map_routes)
    
    app.on_startup.append(startup)
    app.on_startup.append(attach_db)
    

    if app['command_args'].db:
        print("開始變更db 版本")
        app.on_startup.append(handle_db_schema)

    app.on_cleanup.append(cleanup)

    # create data_processing_config.ini
    config_file = open(os.path.join(os.getcwd(), 'app','config','data_processing_config.ini'), 'w', encoding = "utf8")
    config_file.write('[env]\n')
    config_file.write('env_mode = ' + str(app['command_args'].env) + '\n')

    return app
