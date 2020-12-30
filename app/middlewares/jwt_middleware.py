# coding=utf-8
import jwt
from aiohttp.web_request import Request
from aiohttp.web import middleware,json_response
from app.config.models import Account, Map_Garage_To_Account
from app.controllers.login_controller import LoginController
from sqlalchemy import text
import functools

@middleware
async def jwt_middleware(request: Request, handler:functools.partial):
    """ middelware : decode jwt token """
    jwt_token = request.headers.get('authorization', None)
    if request.method=="OPTIONS": #skip pre-flight
        return await handler(request)
    if "/api/doc" in request.rel_url.path:
        return await handler(request)
    elif "/au/" in request.rel_url.path:
        return await handler(request)
    elif handler.__func__==LoginController.login: 
        return await handler(request)
    elif jwt_token is not None:
        try:
            payload = jwt.decode(jwt_token, request.app['jwt_secret'],
                                    algorithms=[request.app['jwt_algorithm']])
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            return json_response({'message': 'Token is invalid'}, status=403)
        
        async with request.app['pmsdb'].acquire() as conn:
            user = await conn.execute(text("select * from account where account_id=:account_id limit 1"), {'account_id':payload['id']})
                
            if user is None:
                return json_response({'message': 'can not find user'}, status=403)

            one = await user.fetchone()
            if one is None:
                return json_response({'message': 'can not find user'}, status=403)

           
            request['login'] = one
            request.app['garage_group'] = await getGarageGroup(request, payload['id'])
            request.app['role_permission'] = await getPermission(request, one['role_id'])
            permission_list = []

            for i in request.app['role_permission']:
                permission_list.append(i['permission_id'])
            return await handler(request)
    else:
        return json_response({'message': 'Token is invalid'}, status=403)

async def getGarageGroup(request,id):
    async with request.app['pmsdb'].acquire() as conn:
        x = await conn.execute(
            text("select g.garage_group_id ,g.garage_group_name from map_garage_group_to_account a left join garage_group g on a.garage_group_id = g.garage_group_id where account_id =:id"
            ),{'id':id})
            
        garage_group = [dict(row.items()) async for row in await conn.execute(
            text("select g.garage_group_id ,g.garage_group_name from map_garage_group_to_account a left join garage_group g on a.garage_group_id = g.garage_group_id where account_id =:id"
           ),{'id':id})
        ]
        return garage_group

async def getPermission(request,role_id):
    async with request.app['pmsdb'].acquire() as conn:
        permission = [dict(row.items()) async for row in await conn.execute(text("select p.* from map_role_permission mp left join permission p on mp.permission_id = p.permission_id where mp.role_id =:role_id"),{'role_id':role_id})]
        return permission
