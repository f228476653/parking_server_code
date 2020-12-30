import os,sys,asyncio
sys.path.append(os.path.join(os.getcwd()))
from app.config.settings import Settings
from configparser import ConfigParser
from aiomysql.sa import create_engine

environment_settings = None

class Config:
    async def read_env(self):
        cfg = ConfigParser()
        cfg.read(os.path.join(os.getcwd(), 'app','config','data_processing_config.ini'))
        env_mode = cfg.get('env','env_mode')
        data_processing = True

        environment_settings = Settings()
        await environment_settings.load_environment(env_mode, data_processing)
        return environment_settings

    async def db_engine(self):
        environment_settings = await self.read_env()
        pmsplus_db = await create_engine(
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
        return pmsplus_db