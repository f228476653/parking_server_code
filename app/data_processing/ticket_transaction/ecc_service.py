import asyncio
import os, glob, shutil, sys, operator
import time, datetime
sys.path.append(os.path.join(os.getcwd()))
from app.config.models import Trx_Data, TicketTransactionFtpConfig
from app.util.implicit_ftp_tls import ImplicitFTP_TLS
from app.config.logger import LogConfig

logger = LogConfig.get_logger()

class ECCService:
    _db = None
    _semaphore = None
    _file_directory_path = None
    _now_date = None
    _card_type = None
    _directory_path = None

    def __init__(self, db):
        self._db = db
        self._semaphore = asyncio.Semaphore(10)
        # Windows 測試
        # self._file_directory_path = "D:\\test_use"
        # 正式環境
        self._file_directory_path = "/home/pms_plus/file_directory/"
        self._process_path = os.path.join(self._file_directory_path, "ticket_transaction_files")
        self._now_date = datetime.date.today().strftime("%Y%m%d")
        self._card_type = "ecc"
        self._directory_path = os.getcwd()
        LogConfig.logger_init(os.path.dirname(os.path.abspath(__file__)))

    """ 建立多層目錄 """
    def mkdirs(self, path): 
        # 去除前方空格
        path = path.strip()
        # 去除尾巴 \ 符號
        path = path.rstrip("\\")
        
        # 判斷路徑是否存在
        # 存在     True
        # 不存在   False
        isExists = os.path.exists(path)
        
        # 判断结果
        if not isExists:
            # 建立目錄
            os.makedirs(path)
            # 如果不存在則建立目錄
            return True
        else:
            # 如果目錄存在則不建立
            return False

    async def ecc_get_customer_list(self):
        sql = f"""SELECT distinct 
            a.*, 
            b.customer_code 
            FROM 
            `ticket_transaction_ftp_config` AS a 
            LEFT JOIN 
            `customer` AS b 
            ON 
            a.customer_id = b.customer_id 
            WHERE 
            a.status = 1 
            and a.card_type ='01'"""
        async with self._db.acquire() as conn:
            return [dict(row.items()) async for row in await conn.execute(sql)] , (await conn.execute(sql)).rowcount

    async def feedback_data_semaphore(self, data, length: int):
        if length != 0:
            logger.info("[ECC悠遊卡][回饋檔]，需處理營運商數量： [%s]。" %(length))
            f = await asyncio.wait([self.feedback_data_read_content(data[num]) for num in range(0, length)])
            return f
        else:
            logger.info("[ECC悠遊卡][回饋檔]，無營運商需要處理。")

    async def feedback_data_read_content(self, data):
        await self._semaphore.acquire()
        logger.info("[ECC悠遊卡][回饋檔]，營運商代碼：[%s] 處理中。" %(str(data['customer_code'])))
        # 回饋檔匯入資料庫
        feedback_files_import_db_path = os.path.join(self._process_path, str(data['customer_code']), self._card_type, "feedback_files_import_db")
        self.mkdirs(feedback_files_import_db_path)
        # 回饋檔匯入資料庫備份
        feedback_files_import_db_backup_path = os.path.join(self._process_path, str(data['customer_code']), self._card_type, "feedback_files_import_db_backup", self._now_date)
        self.mkdirs(feedback_files_import_db_backup_path)

        # 回饋檔匯入資料庫失敗
        feedback_files_import_db_failed_backup_path = os.path.join(self._process_path, str(data['customer_code']), self._card_type, "feedback_files_import_db_failed_backup", self._now_date)
        self.mkdirs(feedback_files_import_db_failed_backup_path)

        data_array = []
        # 回饋檔
        for root, folders, files in os.walk(feedback_files_import_db_path):
            for sfile in files:
                if(sfile.startswith("TRNC.")):
                    logger.info("[ECC悠遊卡][回饋檔]，營運商代碼：[%s]，檔案 [%s] 處理中。" %(str(data['customer_code']), sfile))
                    aFile = os.path.join(root, sfile)
                    result = True
                    seq = 0

                    content = open(aFile, 'r', encoding = "utf8")
                    for line in content.readlines():
                        if len(line) == 513:
                            if (operator.eq('D', line[0:1])):
                                feedback_data = {}
                                unix_time = int((line[104:106] + line[102:104] + line[100:102] + line[98:100]), 16)
                                trx_datetime = datetime.datetime.utcfromtimestamp(unix_time)

                                feedback_data['file_name'] = sfile
                                feedback_data['trx_date'] = str(trx_datetime)[0 : 10].replace('-','')
                                feedback_data['trx_time'] = str(trx_datetime)[11 :].replace(':','')
                                feedback_data['card_no'] = int(line[3:20])
                                feedback_data['txn_no'] = int(line[54:62])
                                feedback_data['trx_amt'] = line[62:70]
                                feedback_data['device_id'] = line[20:30]
                                feedback_data['trx_type'] = line[78:84]
                                feedback_data['el_value'] = line[70:78]
                                feedback_data['cal_date'] = line[444:452]
                                # data['cal_status'] = 
                                # data['cal_err_code'] = 
                                feedback_data['trx_sub_type'] = line[86:88]
                                feedback_data['garage_code'] = line[376:381]
                                # data['upload_zip_name'] =
                                feedback_data['feedback_file_name'] = sfile
                                feedback_data['cal_status'] = "F"
                                # data['cal_err_code'] = ""

                                data_array.append(Trx_Data.insert().values(feedback_data))

                                if(len(data_array) == 500):
                                    seq +=1
                                    result = await self.feedback_data_import_db(data_array, str(data['customer_code']), sfile, seq)
                                    data_array.clear()
                                    if result == False:
                                        await self.delete_feedback_data(sfile)
                                        break

                            elif (len(data_array) != 0 and operator.eq('T', line[0:1])):
                                seq += 1
                                result = await self.feedback_data_import_db(data_array, str(data['customer_code']), sfile, seq)
                                data_array.clear()
                                if result == False:
                                    await self.delete_feedback_data(sfile)
                                    break
                    content.close()
                    if result == True:
                        shutil.move(aFile, os.path.join(feedback_files_import_db_backup_path, sfile))
                    else:
                        shutil.move(aFile, os.path.join(feedback_files_import_db_failed_backup_path, sfile))
                    logger.info("[ECC悠遊卡][回饋檔]，營運商代碼：[%s]，檔案 [%s] 處理結束。" %(str(data['customer_code']), sfile))
        logger.info("[ECC悠遊卡][回饋檔]，營運商代碼：[%s] 處理完成。" %(str(data['customer_code'])))
        return self._semaphore.release()

    async def feedback_data_import_db(self, data_array, customer_code, file_name, seq):
        logger.info("[ECC悠遊卡][回饋檔]，營運商代碼：[%s]，檔案 [%s] 處理第 [%s] 次。" %(customer_code, file_name, seq))
        async with self._db.acquire() as conn:
            trans = await conn.begin()
            try:
                for data in data_array:
                    rz =  await conn.execute(data)
            except Exception as e:
                logger.exception(e)
                await trans.rollback()
                raise
                logger.error("[ECC悠遊卡][回饋檔]，營運商代碼：[%s]，檔案 [%s] 處理第 [%s] 次 Failed。" %(customer_code, file_name, seq))
                return False
            else:
                await trans.commit()
                logger.info("[ECC悠遊卡][回饋檔]，營運商代碼：[%s]，檔案 [%s] 處理第 [%s] 次 Success。" %(customer_code, file_name, seq))
                return True

    async def delete_feedback_data(self, file_name, customer_code):
        logger.info("[ECC悠遊卡][回饋檔]，營運商代碼：[%s]，檔案 [%s] 處理異常，刪除已匯入資料。" %(customer_code, file_name))
        async with self._db.acquire() as conn:
            trans = await conn.begin()
            try:
                rz =  await conn.execute(Trx_Data.delete().where(Trx_Data.c.file_name == file_name))
            except Exception as e:
                logger.exception(e)
                await trans.rollback()
                raise
                logger.info("[ECC悠遊卡][回饋檔]，營運商代碼：[%s]，檔案 [%s] 處理異常，刪除已匯入資料 Failed。" %(customer_code, file_name))
            else:
                await trans.commit()
                logger.info("[ECC悠遊卡][回饋檔]，營運商代碼：[%s]，檔案 [%s] 處理異常，刪除已匯入資料 Success。" %(customer_code, file_name))

    async def download_semaphore(self, data, length: int, download_file_type):
        if length != 0:
            if (operator.eq('download_feedback_files', download_file_type)):
                logger.info("[ECC悠遊卡][下載回饋檔]，需處理營運商數量： [%s]。" %(length))
            elif (operator.eq('download_black_list', download_file_type)):
                logger.info("[ECC悠遊卡][下載黑名單]，需處理營運商數量： [%s]。" %(length))
            f = await asyncio.wait([self.download_files(data[num], download_file_type) for num in range(0, length)])
            return f
        else:
            if (operator.eq('download_feedback_files', download_file_type)):
                logger.info("[ECC悠遊卡][下載回饋檔]，無營運商需要處理。")
            elif (operator.eq('download_black_list', download_file_type)):
                logger.info("[ECC悠遊卡][下載黑名單]，無營運商需要處理。")

    async def download_files(self, data, download_file_type):
        await self._semaphore.acquire()
        if (operator.eq('download_feedback_files', download_file_type)):
            logger.info("[ECC悠遊卡][下載回饋檔]，營運商代碼：[%s] 處理中。" %(str(data['customer_code'])))
        elif (operator.eq('download_black_list', download_file_type)):
            logger.info("[ECC悠遊卡][下載黑名單]，營運商代碼：[%s] 處理中。" %(str(data['customer_code'])))
            
        # 檔案下載位置
        download_path = os.path.join(self._process_path, str(data['customer_code']), self._card_type, "download", download_file_type)
        self.mkdirs(download_path)

        # 回饋檔匯入資料庫
        feedback_files_import_db_path = os.path.join(self._process_path, str(data['customer_code']), self._card_type, "feedback_files_import_db")
        self.mkdirs(feedback_files_import_db_path)

        # 供設備下載黑名單位置
        customer_download_black_list_path = os.path.join(self._directory_path, os.path.join('csvs', 'out'), str(data['customer_code']), "ecc.bl")
        self.mkdirs(customer_download_black_list_path)

        try:
            ftp_connection = ImplicitFTP_TLS()
            ftp_connection.connect(str(data['ip_address']), int(data['ip_port']), timeout = 60)
            ftp_connection.login(str(data['account']), str(data['password']))
            ftp_connection.prot_p()

            ticket_host_path = str(data['download_path'])

            # 回饋檔
            if (operator.eq('download_feedback_files', download_file_type)):
                ftp_connection.cwd(ticket_host_path)
                fileList = ftp_connection.nlst()
                for file in fileList:
                    if(file.startswith("TRNC.")):
                        if not os.path.exists(os.path.join(download_path, file)):
                            ftp_connection.retrbinary('RETR %s'%file, open(os.path.join(download_path, file), "wb").write)
                            shutil.copyfile(os.path.join(download_path, file), os.path.join(feedback_files_import_db_path, file))
            # 黑名單
            elif (operator.eq('download_black_list', download_file_type)):
                ftp_connection.cwd("/ftpblc/")
                fileList = ftp_connection.nlst()
                for file in fileList:
                    if(file.startswith("BLC") and file.endswith(".BIG")):
                        if not os.path.exists(os.path.join(download_path, file)):
                            ftp_connection.retrbinary('RETR %s'%file, open(os.path.join(download_path, file), "wb").write)
                            shutil.copyfile(os.path.join(download_path, file), os.path.join(customer_download_black_list_path, file))
                            
            ftp_connection.close()
            if (operator.eq('download_feedback_files', download_file_type)):
                logger.info("[ECC悠遊卡][下載回饋檔]，營運商代碼：[%s] 處理 Success。" %(str(data['customer_code'])))
            elif (operator.eq('download_black_list', download_file_type)):
                logger.info("[ECC悠遊卡][下載黑名單]，營運商代碼：[%s] 處理中 Success。" %(str(data['customer_code'])))
        except Exception as e:
            logger.exception(e)
            if (operator.eq('download_feedback_files', download_file_type)):
                logger.error("[ECC悠遊卡][下載回饋檔]，營運商代碼：[%s] 處理 Failed。" %(str(data['customer_code'])))
            elif (operator.eq('download_black_list', download_file_type)):
                logger.error("[ECC悠遊卡][下載黑名單]，營運商代碼：[%s] 處理中 Failed。" %(str(data['customer_code'])))
        return self._semaphore.release()