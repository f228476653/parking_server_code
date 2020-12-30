from functools import wraps
from aiohttp import web
from pprint import pprint
from app.services.service import Service
from app.custom_errors.permission_error import PermissionError


def check_customer_authorization(is_check: bool):
    """ to check if login user can query other customer's data controller function """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args):
            request = args[-1] 
            account_id=request.match_info['account_id']
            if not await Service.static_is_account_id_in_has_same_customer_id(request.app['pmsdb'],request['login'].customer_id,account_id) :
                raise PermissionError("static_is_account_id_in_has_same_customer_id","not permit to quesry other customer's data")
            return await func(*args)
        return wrapper
    return decorator