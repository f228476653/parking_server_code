import asyncio
import sqlalchemy as sa
import sqlalchemy.orm as orm
import datetime
from sqlalchemy.types import Enum
from aiomysql.sa import create_engine
from sqlalchemy.dialects.mysql import BIGINT, INTEGER

"""
create tables and models
"""
metadata = sa.MetaData()

Customer = sa.Table(
    'customer', metadata,
    sa.Column('customer_id', sa.Integer, primary_key=True),
    sa.Column('customer_code', sa.String(150), unique=True,nullable=False),
    sa.Column('company_name', sa.String(255), unique=False,nullable=False),
    sa.Column('company_english_name', sa.String(255), unique=False,nullable=False),
    sa.Column('company_union_number', sa.String(15), unique=False,nullable=False),
    sa.Column('contact_username', sa.String(150), unique=False,nullable=False),
    sa.Column('contact_datetime', sa.String(10), unique=False,nullable=False),
    sa.Column('mobile', sa.String(30), unique=True, nullable=True),
    sa.Column('fax', sa.String(30), unique=True, nullable=True),
    sa.Column('phone_number1', sa.String(30), unique=True, nullable=True),
    sa.Column('phone_number2', sa.String(30), unique=True, nullable=True),
    sa.Column('email',sa.String(255), unique=True,nullable=True),
    sa.Column('customer_status',sa.Integer, unique=False,nullable=True),
    sa.Column('note',sa.String(255), unique=False,nullable=True),
    sa.Column('contact_availible_datetime',sa.String(255), unique=False,nullable=True),
    sa.Column('company_address',sa.String(255), unique=False,nullable=True),
    sa.Column('create_date', sa.DateTime, default=datetime.datetime.utcnow),
    sa.Column('modified_date', sa.DateTime, default= datetime.datetime.utcnow),
    sa.Column('create_account_id',sa.Integer, unique=False,nullable=False),
    sa.Column('modified_account_id',sa.Integer)
)


Garage = sa.Table(
    'garage', metadata,
    sa.Column('garage_code', sa.String(10), unique=True,nullable=False),
    sa.Column('garage_name', sa.String(50), unique=False,nullable=True),
    sa.Column('customer_id', sa.Integer, unique=False,nullable=True),
    sa.Column('city_name', sa.String(50), unique=False,nullable=True),
    sa.Column('city_code', sa.String(3), unique=False,nullable=True),
    sa.Column('district', sa.String(10), unique=False,nullable=True),
    sa.Column('district_code', sa.String(3), unique=False,nullable=True),
    sa.Column('address1', sa.String(255), unique=False,nullable=True),
    sa.Column('address2', sa.String(255), unique=False,nullable=True),
    sa.Column('total_capacity', sa.Integer,nullable=True),
    sa.Column('sedan_capacity', sa.Integer,nullable=True),
    sa.Column('motocycle_capacity', sa.Integer,nullable=True),
    sa.Column('sedan_priority_pragnant_capacity', sa.Integer,nullable=True),
    sa.Column('motocycle_priority_pragnant_capacity', sa.Integer,nullable=True),
    sa.Column('sedan_priority_disability_capacity', sa.Integer,nullable=True),
    sa.Column('motocycle_priority_disability_capacity', sa.Integer,nullable=True),
    sa.Column('garage_lat',sa.String(50),nullable=True),
    sa.Column('garage_lng',sa.String(50),nullable=True),
    sa.Column('caculation_time_base_unit', sa.Integer,nullable=True),
    sa.Column('charge_infomation',sa.String(1000),nullable=True),
    sa.Column('supplementary_details',sa.String(1000),nullable=True),
    sa.Column('business_hour_begin',sa.String(5) ,nullable=True),
    sa.Column('business_hour_end',sa.String(5),nullable=True),
    sa.Column('number_of_entrance',sa.Integer,nullable=True),
    sa.Column('number_of_exit',sa.Integer,nullable=True),
    sa.Column('number_of_driveway_in',sa.Integer,nullable=True),
    sa.Column('number_of_driveway_out',sa.Integer,nullable=True),
    sa.Column('management_type',sa.Integer,nullable=True),
    sa.Column('garage_type',sa.Integer,nullable=True),
    sa.Column('lot_type',sa.Integer,nullable=True),
    sa.Column('establish_status',sa.Integer,nullable=True),
    sa.Column('max_clearance',sa.String(5),nullable=True),
    sa.Column('on_site_liaison',sa.String(20),nullable=True),
    sa.Column('on_site_phone',sa.String(20),nullable=True),
    sa.Column('on_site_email',sa.String(20),nullable=True),
    sa.Column('on_site_cell_phone',sa.String(20),nullable=True),
    sa.Column('customer_garage_id',sa.String(20),nullable=True),
    sa.Column('current_capacity_sedan',sa.Integer,nullable=True),
    sa.Column('current_capacity_suv',sa.Integer,nullable=True),
    sa.Column('current_capacity_bicycle',sa.Integer,nullable=True),
    sa.Column('current_capacity_motocycle',sa.Integer,nullable=True),
    sa.Column('current_capacity_truck',sa.Integer,nullable=True),
    sa.Column('current_capacity_bus',sa.Integer,nullable=True),
    sa.Column('current_capacity_total',sa.Integer,nullable=True),
    sa.Column('gov_id',sa.String(30), unique=False,nullable=True),
    sa.Column('current_capacity_update_account_id',sa.Integer,nullable=True),
    sa.Column('current_capacity_updatetime',sa.DateTime,nullable=True),
    sa.Column('create_date', sa.DateTime, default=datetime.datetime.utcnow),
    sa.Column('modified_date', sa.DateTime, default= datetime.datetime.utcnow),
    sa.Column('create_account_id',sa.Integer, unique=False,nullable=False),
    sa.Column('modified_account_id',sa.Integer),
    sa.Column('garage_id', sa.Integer, primary_key=True),
    sa.Column('road_code', sa.String(5), nullable=True)
    ,mysql_charset='utf8'
)

GarageGroup = sa.Table(
    'garage_group', metadata,
    sa.Column('garage_group_id', sa.Integer, primary_key=True),
    sa.Column('garage_group_name', sa.String(255), unique=True,nullable=False),
    sa.Column('customer_id', sa.String(50), unique=True,nullable=False),
    sa.Column('parent_id',sa.Integer, default = 0),
    sa.Column('description', sa.String(150), unique=False,nullable=True),
    sa.Column('create_date', sa.DateTime, default=datetime.datetime.utcnow),
    sa.Column('modified_date', sa.DateTime, default= datetime.datetime.utcnow),
    sa.Column('create_account_id',sa.Integer, unique=False,nullable=False),
    sa.Column('modified_account_id',sa.Integer)
    ,mysql_charset='utf8'
)

Map_Garage_To_Garage_Group = sa.Table(
    'map_garage_to_garage_group', metadata,
    sa.Column('garage_id', sa.Integer, unique=True,nullable=False),
    sa.Column('garage_group_id', sa.Integer, unique=True, nullable=False),
    sa.Column('create_date', sa.DateTime, default=datetime.datetime.utcnow),
    sa.Column('modified_date', sa.DateTime, default= datetime.datetime.utcnow),
    sa.Column('create_account_id',sa.Integer, unique=False,nullable=False),
    sa.Column('modified_account_id',sa.Integer)
)

Map_Garage_Group_To_Account = sa.Table(
    'map_garage_group_to_account', metadata,
    sa.Column('garage_group_id', sa.Integer, unique=True,nullable=False),
    sa.Column('account_id', sa.Integer, unique=True, nullable=False)
)
SystemConfiguration = sa.Table(
    'system_configuration', metadata,
    sa.Column('key', sa.String(50), nullable = False),
    sa.Column('value', sa.String(50), nullable = False),
    sa.Column('description', sa.String(100), nullable = False),
    sa.Column('config_group_name', sa.String(50), nullable = False)
)


Map_Garage_To_Account = sa.Table(
    'map_garage_to_account', metadata,
    sa.Column('garage_id', sa.Integer, unique=True,nullable=False),
    sa.Column('account_id', sa.Integer, unique=True, nullable=False)
)

Account = sa.Table(
    'account', metadata,
    sa.Column('account_id', sa.Integer, primary_key=True),
    sa.Column('account', sa.String(255), unique=True,nullable=False),
    sa.Column('customer_id',sa.String(50),nullable=True),
    sa.Column('password', sa.String(1000), unique=False,nullable=False),
    sa.Column('user_first_name', sa.String(255), unique=True, nullable=True),
    sa.Column('user_middle_name', sa.String(255), unique=True, nullable=True),
    sa.Column('user_last_name', sa.String(255), unique=True, nullable=True),
    sa.Column('email',sa.String(255), unique=True,nullable=True),
    sa.Column('mobile',sa.String(255), unique=True,nullable=True),
    sa.Column('role_id',sa.Integer, sa.ForeignKey('role.role_id'), unique=False,nullable=False),
    sa.Column('is_superuser', sa.Boolean(), default=False, nullable=False),
    sa.Column('is_customer_root', sa.Boolean(), default=False, nullable=False),
    sa.Column('is_api_user', sa.Boolean(), default=False, nullable=False),
    sa.Column('create_date', sa.TIMESTAMP, default=datetime.datetime.timestamp),
    sa.Column('modified_date', sa.TIMESTAMP, default= datetime.datetime.timestamp),
    sa.Column('create_account_id',sa.Integer, unique=False,nullable=False),
    sa.Column('modified_account_id',sa.Integer)
)


Permission = sa.Table(
    'permission', metadata,
    sa.Column('permission_id', sa.Integer, primary_key=True),
     sa.Column('name', sa.String(255), unique=True,nullable=False),
    sa.Column('description', sa.String(255), unique=False, nullable=False),
    sa.Column('permission_type', sa.String(255), unique=False, nullable=False),
    sa.Column('parent_id',sa.Integer,unique=False,nullable=True),
    sa.Column('enable',sa.Integer,unique=False,nullable=False),
    sa.Column('create_date', sa.DateTime, default=datetime.datetime.utcnow),
    sa.Column('modified_date', sa.DateTime, default= datetime.datetime.utcnow),
    sa.Column('create_account_id',sa.Integer),
    sa.Column('modified_account_id',sa.Integer)
)
 
Role = sa.Table(
    'role', metadata,
    sa.Column('role_id', sa.Integer, primary_key=True),
    sa.Column('name', sa.String(255), unique=True,nullable=False),
    sa.Column('description', sa.String(255), unique=True, nullable=False),
    sa.Column('role_type', sa.String(255), unique=True, nullable=False),
    sa.Column('is_system_role', sa.Integer, unique=False,nullable=False,default=0),
    sa.Column('customer_id', sa.Integer),
    sa.Column('create_date', sa.DateTime, default=datetime.datetime.utcnow),
    sa.Column('modified_date', sa.DateTime, default= datetime.datetime.utcnow),
    sa.Column('create_account_id',sa.Integer, unique=False,nullable=False),
    sa.Column('modified_account_id',sa.Integer)
)

Map_Role_Permission = sa.Table(
    'map_role_permission', metadata,
    sa.Column('role_id', sa.Integer, unique=True,nullable=False),
    sa.Column('permission_id', sa.Integer, unique=True, nullable=False),
    sa.Column('create_date', sa.DateTime, default=datetime.datetime.utcnow),
    sa.Column('modified_date', sa.DateTime, default= datetime.datetime.utcnow),
    sa.Column('create_account_id',sa.Integer, unique=False,nullable=False),
    sa.Column('modified_account_id',sa.Integer)
)


Map_Garage_To_System_Config = sa.Table(
    'map_garage_to_system_config', metadata,
    sa.Column('map_garage_to_system_config_id', sa.Integer, unique=True,nullable=False,primary_key=True),
    sa.Column('garage_id', sa.String(60), unique=True,nullable=False),
    sa.Column('system_config_id', sa.Integer, default=0),
    sa.Column('modified_account_id', sa.Integer),
    sa.Column('modified_date', sa.DateTime)
)


Event = sa.Table(
    'event', metadata,
    sa.Column('event_id', sa.Integer, unique=True,nullable=False),
    sa.Column('SystemEventType', sa.Integer, unique=False,nullable=False),
    sa.Column('event_subtype', sa.Integer, unique=False,nullable=False),
    sa.Column('description', sa.String(255), unique=False, nullable=False)
)

SystemLog = sa.Table(
    'system_log', metadata,
    sa.Column('system_log_id', sa.Integer, unique=True,nullable=False,primary_key=True),
    sa.Column('event_id', sa.Integer, unique=False,nullable=False),
    sa.Column('create_account_id',sa.Integer, unique=False,nullable=False),
    sa.Column('create_date', sa.DateTime, default=datetime.datetime.utcnow),
    sa.Column('event_message', sa.String(2000), unique=False, nullable=False),
    sa.Column('query_string', sa.String(255), unique=False, nullable=True),
    sa.Column('field_1', sa.String(255), unique=False, nullable=False)
)

ForgetPassword = sa.Table(
    'forget_password', metadata,
    sa.Column('no', sa.Integer, unique=True, nullable=False, primary_key=True),
    sa.Column('account_id', sa.Integer, nullable=False),
    sa.Column('account', sa.String(50), nullable=False),
    sa.Column('email', sa.Integer, nullable=False),
    sa.Column('token', sa.String(500), nullable=False),
    sa.Column('create_date', sa.DateTime, nullable=True, default = datetime.datetime.utcnow),
    sa.Column('has_change_pwd', sa.Integer, nullable=True),
    sa.Column('expiration_date', sa.DateTime, nullable=True)
)