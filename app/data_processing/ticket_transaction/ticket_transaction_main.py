import os, sys, asyncio, operator
sys.path.append(os.path.join(os.getcwd()))
from ecc_service import ECCService
from app.data_processing.config.config import Config

async def db_engine():
    global db
    service = Config()
    db = await service.db_engine()

async def ecc_feedback_data_parse():
    service = ECCService(db)
    customer_list = await service.ecc_get_customer_list()
    customer_list_data = customer_list[0]
    customer_list_length = customer_list[1]
    await service.feedback_data_semaphore(customer_list_data, customer_list_length)

async def ecc_download_feedback_files(download_type):
    service = ECCService(db)
    customer_list = await service.ecc_get_customer_list()
    customer_list_data = customer_list[0]
    customer_list_length = customer_list[1]
    await service.download_semaphore(customer_list_data, customer_list_length, download_type)

async def ecc_download_black_list(download_type):
    service = ECCService(db)
    customer_list = await service.ecc_get_customer_list()
    customer_list_data = customer_list[0]
    customer_list_length = customer_list[1]
    await service.download_semaphore(customer_list_data, customer_list_length, download_type)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(db_engine())
    if (operator.eq(sys.argv[1], "ecc")):
        if (operator.eq(sys.argv[2], "feedback_data_parse")):
            loop.run_until_complete(ecc_feedback_data_parse())
        elif (operator.eq(sys.argv[2], "download_feedback_files")):
            loop.run_until_complete(ecc_download_feedback_files(sys.argv[2]))
        elif (operator.eq(sys.argv[2], "download_black_list")):
            loop.run_until_complete(ecc_download_black_list(sys.argv[2]))
    db.close()

