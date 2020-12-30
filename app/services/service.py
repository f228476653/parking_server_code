
from sqlalchemy import desc,text
from app.custom_errors.api_error_data import *
class Service:
    
    @staticmethod
    async def static_is_account_id_in_has_same_customer_id(db,customer_id:int,account_id: int) -> bool:
        """ where user query by account_id , we must check if the account_id has same cutomer_id to the login user's account_id"""
        async with db.acquire() as conn:
            sql = """select * from account where account_id =:account_id and customer_id =:customer_id """

            condition = { 
                "account_id": account_id,
                "customer_id": customer_id
            }
            result = [dict(row.items()) async for row in await conn.execute(text(sql), condition)]
            return len(result) >0 and True or False

    async def is_account_id_in_has_same_customer_id(self,customer_id:int,account_id: int) -> bool:
        """ where user query by account_id , we must check if the account_id has same cutomer_id to the login user's account_id"""
        async with self._db.acquire() as conn:
            sql = """select * from account where account_id =:account_id and customer_id =:customer_id """

            condition = { 
                "account_id": account_id,
                "customer_id": customer_id
            }
            result = [dict(row.items()) async for row in await conn.execute(text(sql), condition)]
            return len(result) >0 and True or False

    async def is_account_has_authorization_to_use_garage(self, customer_id: int):
        """ 驗證廠商是否有此場站 """
        async with self._db.acquire() as conn:
            sql = """ select garage_id from garage where customer_id = :customer_id """
            condition = {"customer_id": customer_id}
            result = [dict(row.items()) async for row in await conn.execute(text(sql), condition)]
            print(customer_id)
            print(len(result))
            print('********************************************')
            return (len(result) > 0 or customer_id is 0) and True or False
            
    async def is_account_in_has_same_customer_id(self,customer_id:int,account: str) -> bool:
        """ where user query by account_id , we must check if the account_id has same cutomer_id to the login user's account_id"""
        async with self._db.acquire() as conn:
            sql = """select * from account where account =:account and customer_id =:customer_id """

            condition = { 
                "account": account,
                "customer_id": customer_id
            }
            result = [dict(row.items()) async for row in await conn.execute(text(sql), condition)]
            return len(result) >0 and True or False
