import subprocess
from app.config.models import Permission, Map_Role_Permission
class DBVersionControl():
    
    engine = None
    # version_control mapping methods
    version = [1.0]

    def __init__(self, engine):
        self.engine = engine
    
    def is_correct_version_number(self, start, end= version[-1]):
        if start in self.version and end in self.version:
            return {"is_corrent": True, "index_start": self.version.index(start) + 1, "index_end": self.version.index(end)}
        else:
            return {"is_corrent": False, "version_start": start, "version_end": end}

    async def V0_0(self):
        # init 才會執行 刪掉已存在table
        async with self.engine.acquire() as conn:
            await conn.execute('DROP TABLE IF EXISTS system_configuration') 
            await conn.execute('DROP TABLE IF EXISTS account')
            await conn.execute('DROP TABLE IF EXISTS customer')
            await conn.execute('DROP TABLE IF EXISTS permission')
            await conn.execute('DROP TABLE IF EXISTS role')
            await conn.execute('DROP TABLE IF EXISTS garage')
            await conn.execute('DROP TABLE IF EXISTS garage_group')
            await conn.execute('DROP TABLE IF EXISTS map_role_permission')
            await conn.execute('DROP TABLE IF EXISTS  map_garage_group_to_account')
            await conn.execute('DROP TABLE IF EXISTS system_log')
            await conn.execute('DROP TABLE IF EXISTS event')

    async def v1_0(self):
        async with self.engine.acquire() as conn:
            await conn.execute('''CREATE TABLE map_garage_group_to_account (
                garage_group_id int,
                account_id int
                )DEFAULT CHARSET=utf8
            ''')
           

            await conn.execute(''' CREATE TABLE system_configuration (
                `key` varchar(50) NOT NULL COMMENT '系統配置名稱',
                `value` varchar(50) NOT NULL COMMENT '系統配置值',
                `description` varchar(100) NOT NULL COMMENT '用途描述',
                `config_group_name` varchar(50) NOT NULL COMMENT '系統配置群組名稱',
                PRIMARY KEY  (`key`)
                ) DEFAULT CHARSET=utf8 ''')


            await conn.execute('''CREATE TABLE account (
                account_id SERIAL PRIMARY KEY,
                create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified_date TIMESTAMP,
                create_account_id int,
                modified_account_id int,
                account VARCHAR(80) NOT NULL,
                customer_id int,
                password VARCHAR(500) NOT NULL,
                user_first_name VARCHAR(100) NULL,
                user_middle_name VARCHAR(100) NULL,
                user_last_name VARCHAR(100) NULL,
                email VARCHAR(100) NULL,
                mobile VARCHAR(100) NULL,
                role_id int,
                is_api_user BOOLEAN NOT NULL DEFAULT FALSE,
                is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
                is_customer_root BOOLEAN NOT NULL DEFAULT FALSE
            ) DEFAULT CHARSET=utf8''')

           

            await conn.execute('''CREATE TABLE customer (
                customer_id SERIAL PRIMARY KEY,
                create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified_date TIMESTAMP,
                create_account_id int,
                modified_account_id int,
                company_english_name VARCHAR(255),
                company_union_number VARCHAR(15),
                customer_code VARCHAR(150) NOT NULL,
                company_name VARCHAR(150) NOT NULL,
                contact_username VARCHAR(150) NOT NULL,
                mobile VARCHAR(30) NULL,
                fax VARCHAR(30) NULL,
                phone_number1 VARCHAR(30) NULL,
                phone_number2 VARCHAR(30) NULL,
                email VARCHAR(100) NULL,
                customer_status int NULL COMMENT '閘門控制模式(1:active, 0:disabled)',
                note VARCHAR(255) NULL,
                contact_availible_datetime VARCHAR(255) NULL,
                contact_datetime VARCHAR(10),
                company_address VARCHAR(255)
            ) DEFAULT CHARSET=utf8''')


            await conn.execute('''CREATE TABLE permission (
                permission_id SERIAL PRIMARY KEY,
                create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified_date TIMESTAMP,
                create_account_id int,
                modified_account_id int,
                name VARCHAR(50) NOT NULL,
                description VARCHAR(255) NULL,
                permission_type VARCHAR(255) NOT NULL,
                parent_id int,
                enable int Default 1
            ) DEFAULT CHARSET=utf8''')


            await conn.execute('''CREATE TABLE role (
                role_id SERIAL PRIMARY KEY,
                create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified_date TIMESTAMP,
                create_account_id int,
                modified_account_id int,
                name VARCHAR(50) NOT NULL,
                description VARCHAR(255) NULL,
                role_type VARCHAR(30) NOT NULL,
                is_system_role int Default 0 COMMENT '只有is_superuser =1 的帳號才能夠選擇的角色',
                customer_id  int
                )DEFAULT CHARSET=utf8
            ''')

            await conn.execute('''CREATE TABLE map_role_permission (
                create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified_date TIMESTAMP,
                create_account_id int,
                modified_account_id int,
                role_id int,
                permission_id int
                )DEFAULT CHARSET=utf8
            ''')

            await conn.execute('''CREATE TABLE garage (
                garage_code VARCHAR(10) NOT NULL COMMENT 'Acer ITS defined garage code',
                garage_name VARCHAR(50) NULL,
                customer_id int,
                city_name VARCHAR(50) NULL,
                city_code VARCHAR(3) NULL,
                district VARCHAR(10) NULL,
                district_code VARCHAR(3) NULL,
                address1 VARCHAR(255) NULL,
                address2 VARCHAR(255) NULL,
                total_capacity int DEFAULT 0,
                sedan_capacity int DEFAULT 0,
                motocycle_capacity int DEFAULT 0,
                sedan_priority_pragnant_capacity int DEFAULT 0,
                motocycle_priority_pragnant_capacity int DEFAULT 0,
                sedan_priority_disability_capacity int DEFAULT 0,
                motocycle_priority_disability_capacity int DEFAULT 0,
                garage_lat VARCHAR(50),
                garage_lng VARCHAR(50),
                caculation_time_base_unit int DEFAULT 0 COMMENT '分:0/秒:1',
                charge_infomation VARCHAR(1000) NULL,
                supplementary_details VARCHAR(1000) NULL,
                business_hour_begin VARCHAR(5),
                business_hour_end VARCHAR(5),
                number_of_entrance int Default 0,
                number_of_exit int Default 0,
                number_of_driveway_in int Default 0,
                number_of_driveway_out int Default 0,
                management_type int Default 0 COMMENT '0:固定都有管理員/2:不定時巡視管理員/3:無管理員',
                garage_type int COMMENT '0:平面、1:車塔、2:機械、3:平面/機械混合、4:地下室',
                lot_type int COMMENT '室內還是室外停車場 室內:0/室外:1',
                establish_status int COMMENT '建置狀態 完成:0/建置中:1',
                max_clearance VARCHAR(5) COMMENT '車高限制',
                on_site_liaison VARCHAR(20) COMMENT '現場聯絡人',
                on_site_phone VARCHAR(20) COMMENT '現場聯絡電話',
                on_site_email VARCHAR(20) COMMENT '現場email',
                on_site_cell_phone VARCHAR(20) COMMENT '場站電話',
                customer_garage_id VARCHAR(20) COMMENT '客戶自己系統的場站id',
                create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified_date TIMESTAMP,
                create_account_id int,
                modified_account_id int,
                garage_id SERIAL PRIMARY KEY
                )DEFAULT CHARSET=utf8
            ''')

            await conn.execute('''CREATE TABLE garage_group (
                garage_group_id SERIAL PRIMARY KEY,
                create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified_date TIMESTAMP,
                create_account_id int,
                modified_account_id int,
                garage_group_name VARCHAR(255) NULL,
                customer_id int,
                parent_id int,
                description VARCHAR(1000) NULL
                )DEFAULT CHARSET=utf8
            ''')


            await conn.execute('''CREATE TABLE system_log (
                system_log_id SERIAL PRIMARY KEY,
                event_id int,
                create_account_id int,
                create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                event_message VARCHAR(255) NULL,
                query_string VARCHAR(255) NULL,
                field_1 VARCHAR(255)
                )DEFAULT CHARSET=utf8
            ''')

            await conn.execute('''CREATE TABLE event (
                event_id SERIAL PRIMARY KEY,
                SystemEventType int,
                event_subtype int,
                description VARCHAR(255) NULL
                )DEFAULT CHARSET=utf8
            ''')

