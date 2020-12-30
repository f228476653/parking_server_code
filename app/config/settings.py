"""Settings module."""

from os import environ
from os.path import join
from os.path import dirname

from dotenv import load_dotenv

class Settings:
    SETTINGS = None
    def _basepath(*args):
        return join(dirname(__file__), '../../', *args)

    async def load_environment(self,env="develop", data_processing = False):
        """Load env.{scope} file."""
        load_dotenv(Settings._basepath('config', 'env.{}'.format(
            environ.get('APP_ENV', env)
        )))
        
        self.SETTINGS = {
            'mongo': {
                'uri': environ.get('MONGO_URI'),
                'db': environ.get('MONGO_DB'),
            },
            'mysql':{
                'host': environ.get('MYSQL_HOST'),
                'dbname': environ.get('MYSQL_DBNAME'),
                'port': environ.get('MYSQL_PORT'),
                'username': environ.get('MYSQL_USERNAME'),
                'passwd': environ.get('MYSQL_PASSWD'),
                'autocommit': environ.get('MYSQL_AUTOCOMMIT')
            },
            'pay_agent': {
                'pklot': {'host': environ.get('PKLOT_HOST', "https://partner-api-sandbox.parkinglotapp.com/"),
                          'token': environ.get('PKLOT_TOKEN',
                                               "Bearer 2f7ae5383a14afe6ab022d39494d0f79cdcb87bb8084fe9adc065449251ac179")
                          }

            }

        }

        if (data_processing == False):
            print(f'AioHttp Server is running in [ {env} ] Mode')
