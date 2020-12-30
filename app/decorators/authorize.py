from functools import wraps
from aiohttp import web
import json

def authorize(*permission):
    """ authorize controller function
    user can use authorize(['1','2']) to check if user owns authority 1 and 2
    """
    def decorator(func):
        """decorator"""
        @wraps(func)
        async def wrapper(*args):
            """ decoration wrapper"""
            request = args[-1]  # TODO @ray_yen check user permission
            or_list = permission[0]
            and_list = permission[1]
            permission_list = []
            for i in request.app['role_permission']:
                permission_list.append(i['permission_id'])
            for i in or_list:
                if i in permission_list:
                    return await func(*args)
            # check = True
            for i in and_list:
                if not i in permission_list:
                    raise PermissionError("錯囉","錯囉")
            return await func(*args)      
            # print('結束 !!!')
            # return await func(*args)  # TODO if raise web.HTTPForbidden()
        return wrapper
    return decorator
