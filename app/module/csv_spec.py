
import time
import datetime

class CsvSpec():
    # TODO 改名換資料夾
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    ibox_pv3_key = ["iCash.csv", "iPass.csv", "YHDP.csv", "IPTable.csv", "setting.csv",
    "switch.csv", "PV.csv", "PMS.csv", "Car.csv", "Receipt.csv", "Server.csv"]
    # ibox_service_data_key = ["iPass.csv", "PMS.csv", "PV.csv", "YHDP.csv"]
    def get_pv3_export_csv_data(self, c_data: dict, g_data: dict, d_data: dict, garage_code: str, customer_code: str, system_configuration: dict, device_type= "pv3"):
        export_data = {}
        result = [self.get_iCash_csv(c_data, g_data, d_data), self.get_iPass_csv(c_data, g_data, d_data),
        self.get_YHDP_csv(c_data), self.get_ip_table_csv(d_data), self.get_setting_csv(g_data, d_data),
        self.get_switch_csv(d_data), self.get_pv_csv(d_data), self.get_pms_csv(c_data, d_data, garage_code, customer_code, system_configuration), self.get_car_csv(),
        self.get_receipt_csv(g_data, d_data), self.get_server_csv(customer_code, garage_code, g_data["store_no"], d_data["driveway"], d_data["eid_pos_no"], device_type, system_configuration)]
        # service_result = [self.get_service_ipass_csv(c_data), self.get_service_pms_csv(c_data),
        # self.get_service_pv_csv(d_data), self.get_service_YHDP_csv(c_data)]
        export_data["pv"] = dict(zip(self.ibox_pv3_key, result))
        # export_data["host"] = dict(zip(self.ibox_service_data_key, service_result))
        return export_data

    #   fee part
    def get_full_fee_args_export_csv_data(self, fee_primary_args, fee_normal_args, fee_special_args):
        # 組出費率csv檔 acer version 
        full_fee_args_keys = ["Fee_Set.csv", "Holiday.csv", "NormalDay.csv", "S_Holiday.csv", "S_NormalDay.csv"]
        result = [self.get_full_fee_set_csv(fee_primary_args), self.get_full_normalday_csv(fee_normal_args["normal"], "normal_day"), 
            self.get_full_normalday_csv(fee_normal_args["holiday"], "holiday"), self.get_full_special_csv(fee_special_args["normal"], "normal_day"),
            self.get_full_special_csv(fee_special_args["holiday"], "holiday")]
        export_data = dict(zip(full_fee_args_keys, result))
        return export_data
        
    def get_full_fee_set_csv(self, fee_primary_args: dict):
        result = {"Version": "N1", "NormalDay": fee_primary_args["normal"], "Holiday": fee_primary_args["holiday"]}
        print("現在處理Fee_Set_csv", result)
        print("====================================")
        return result
        
    def get_full_normalday_csv(self, fee_normal_args: dict, day_type: str):
        result = {"mode": fee_normal_args["mode"], "mode_method": fee_normal_args["mode_method"], "mode_time": fee_normal_args["mode_time"],
        "Max_Fee": fee_normal_args["max_fee"], "Max_Fee_time": fee_normal_args["max_fee_time"], "Free_time": fee_normal_args["free_time"],
        "loop_mode": fee_normal_args["loop_mode"], "First_period_total": fee_normal_args["first_period_total"], "First_period": fee_normal_args["first_period"],
        "First_period_Fee": fee_normal_args["first_period_fee"], "Second_period_total": fee_normal_args["second_period_total"], "Second_period": fee_normal_args["second_period"],
        "Second_period_Fee": fee_normal_args["second_period_fee"], "Third_period_total": fee_normal_args["third_period_total"], "Third_period": fee_normal_args["third_period"],
        "Third_period_Fee": fee_normal_args["third_period_fee"], "_1_Fee_time_start": fee_normal_args["interval_1_fee_time_start"], "_1_Fee_time_end": fee_normal_args["interval_1_fee_time_end"],
        "_1_period": fee_normal_args["interval_1_period"], "_1_Fee": fee_normal_args["interval_1_fee"], "_1_End_method": fee_normal_args["interval_1_end_method"],
        "_2_Fee_time_start": fee_normal_args["interval_2_fee_time_start"], "_2_Fee_time_end": fee_normal_args["interval_2_fee_time_end"], "_2_period": fee_normal_args["interval_2_period"],
        "_2_Fee": fee_normal_args["interval_2_fee"], "_2_End_method": fee_normal_args["interval_2_end_method"], "_3_other_period": fee_normal_args["interval_3_other_period"],
        "_3_other_Fee": fee_normal_args["interval_3_fee"], "_3_End_method": fee_normal_args["interval_3_end_method"]}
        print("現在處理Fee_normal_csv %s %s" % (day_type, result))
        print("====================================")
        return result

    def get_full_special_csv(self, fee_special_args: dict, day_type: str):
        result = {"_1_On_OFF": fee_special_args["on_off_1"], "_1_mode_method": fee_special_args["mode_method_1"], "_1_start_time": fee_special_args["start_time_1"],
        "_1_End_time": fee_special_args["end_time_1"], "_1_Max_Fee": fee_special_args["max_fee_1"], "_1_Free_time": fee_special_args["free_time_1"],
        "_1_First_period_total": fee_special_args["first_period_total_1"], "_1_First_period": fee_special_args["first_period_1"], "_1_First_period_Fee": fee_special_args["first_period_fee_1"],
        "_1_Second_period_total": fee_special_args["second_period_total_1"], "_1_Second_period": fee_special_args["second_period_1"], "_1_Second_period_Fee": fee_special_args["second_period_fee_1"],
        "_1_Third_period_total": fee_special_args["third_period_total_1"], "_1_Third_period": fee_special_args["third_period_1"], "_1_Third_period_Fee": fee_special_args["third_period_fee_1"],
        "_2_On_OFF": fee_special_args["on_off_2"], "_2_mode_method": fee_special_args["mode_method_2"], "_2_start_time": fee_special_args["start_time_2"],
        "_2_End_time": fee_special_args["end_time_2"], "_2_Max_Fee": fee_special_args["max_fee_2"], "_2_Free_time": fee_special_args["free_time_2"],
        "_2_First_period_total": fee_special_args["first_period_total_2"], "_2_First_period": fee_special_args["first_period_2"], "_2_First_period_Fee": fee_special_args["first_period_fee_2"],
        "_2_Second_period_total": fee_special_args["second_period_total_2"], "_2_Second_period": fee_special_args["second_period_2"], "_2_Second_period_Fee": fee_special_args["second_period_fee_2"],
        "_2_Third_period_total": fee_special_args["third_period_total_2"], "_2_Third_period": fee_special_args["third_period_2"], "_2_Third_period_Fee": fee_special_args["third_period_fee_2"]}
        print("現在處理Fee_normal_csv %s %s" % (day_type, result))
        print("====================================")
        return result

    def get_fee_args_export_csv_data(self, fee_rule: dict, fee_para1: dict, fee_para2: dict):
        # 組出費率csv檔
        fee_args_keys = ["Fee_Rule.csv", "NormalDay.csv", "Holiday.csv"]
        result = [self.get_fee_rule_csv(fee_rule), self.get_fee_para_csv(fee_para1, "normal_day"), self.get_fee_para_csv(fee_para2, "holiday")]
        export_data = dict(zip(fee_args_keys, result))
        return export_data
    
    def get_fee_rule_csv(self, fee_rule: dict):
        result = {"New_Car_Hour": fee_rule["new_car_hour"], "period": fee_rule["period"], "NormalDay": fee_rule["normal_day"],
        "Holiday": fee_rule["holiday"], "free_time": fee_rule["free_time"], "mode": fee_rule["fee_mode"]}
        print("現在處理FeeRule_csv", result)
        print("====================================")
        return result

    def get_fee_para_csv(self, fee_para: dict, para_day: str):
        result = {"1_HourPeriod_Fee": fee_para["hour_period_fee1"], "1_HourPeriod_Fee_Start": fee_para["hour_period_fee1_start"],
        "1_HourPeriod_Fee_End": fee_para["hour_period_fee1_end"], "2_HourPeriod_Fee": fee_para["hour_period_fee2"],
        "2_HourPeriod_Fee_Start": fee_para["hour_period_fee2_start"], "2_HourPeriod_Fee_End": fee_para["hour_period_fee2_end"],
        "Max_Fee": fee_para["max_fee"], "Max_Fee_Hour": fee_para["max_hour"], "special_rule": fee_para["special_rule"],
        "special_Fee_Start": fee_para["special_fee_start"], "special_Fee_End": fee_para["special_fee_end"], "special_Fee_Max": fee_para["special_fee_max"],
        "special_Fee_Hour": fee_para["special_fee_hour"], "monthly_pass": fee_para["monthly_pass"]}
        if para_day == "normal_day":
            print("現在處理NormalDay_csv", result)
        elif para_day == "holiday":
            print("現在處理Holiday_csv", result)
        print("====================================")
        return result

    # device_ibox Part
    def get_ibox_export_csv_data(self, c_data: dict, g_data: dict, d_data: dict, garage_code: str, customer_code: str, system_configuration: dict, device_type= "ibox"):
        export_data = {}
        result = [self.get_iCash_csv(c_data, g_data, d_data), self.get_iPass_csv(c_data, g_data, d_data),
        self.get_YHDP_csv(c_data), self.get_ip_table_csv(d_data), self.get_setting_csv(g_data, d_data),
        self.get_switch_csv(d_data), self.get_pv_csv(d_data), self.get_pms_csv(c_data, d_data, garage_code, customer_code, system_configuration), self.get_car_csv(),
        self.get_receipt_csv(g_data, d_data), self.get_server_csv(customer_code, garage_code, g_data["store_no"], d_data["driveway"], d_data["eid_pos_no"], device_type, system_configuration)]
        # service_result = [self.get_service_ipass_csv(c_data), self.get_service_pms_csv(c_data),
        # self.get_service_pv_csv(d_data), self.get_service_YHDP_csv(c_data)]
        export_data["pv"] = dict(zip(self.ibox_pv3_key, result))
        # export_data["host"] = dict(zip(self.ibox_service_data_key, service_result))
        return export_data

    def get_iCash_csv(self, c_data: dict, g_data: dict, d_data: dict):
        result = {"MarketCode" : c_data["market_code"], "Store_No": g_data["store_no"], "Pos_No": d_data["pos_no"], "Cashier_No": c_data["cashier_no"]}
        print("現在處理iCash_csv", result)
        print("====================================")
        return result

    def get_iPass_csv(self, c_data: dict, g_data: dict, d_data: dict):
        result = {"SystemID" : c_data["system_id"], "CompID":  c_data["comp_id"],
        "PLID": g_data["plid"], "Machine": c_data["machine"], "EXTERNAL_IP": d_data["external_ip"],
        "WaterLV_Host": c_data["ipass_water_lv_host"], "WaterLV_Port": c_data["ipass_water_lv_port"],
        "Socket_IP": c_data["socket_ip"]}
        print("現在處理iPass_csv", result)
        print("====================================")
        return result

    def get_YHDP_csv(self, c_data: dict):
        result = {"TransactionSystemID" : c_data["transaction_system_id"], "LOC_ID":  c_data["loc_id"],
        "TransactionTerminalNO": c_data["transaction_terminal_no"], "TID": c_data["tid"],
        "MID": c_data["mid"], "WaterLV": c_data["YHDP_water_lv"], "WaterLV_Host": c_data["YHDP_water_lv_host"],
        "WaterLV_Port": c_data["YHDP_water_lv_port"], "NII": c_data["nii"]}
        print("現在處理YHDP_csv", result)
        print("====================================")
        return result

    def get_ip_table_csv(self, d_data: dict):
        result = {"IPASS": "smallpay.test.i-pass.com.tw,2222,park_41FF,9eef4187", "CarIn": d_data["car_in"], "CarOut": d_data["car_out"]}        
        print("現在處理ip_table_csv", result)
        print("====================================")
        return result

    def get_setting_csv(self, g_data: dict, d_data: dict):
        result = {"Date": self.date, "Station_InOut": d_data["station_inout"],
        "Printer": d_data["printer"], "Store_No": g_data["store_no"],
        "Pos_No": d_data["pos_no"], "Tax_ID_Num": g_data["tax_id_num"], "NTP_Server": g_data["ntp_server"]}
        print("現在處理setting_csv", result)
        print("====================================")
        return result

    def get_switch_csv(self, d_data: dict):
        # !!! 特別處理 !!!
        card_order = d_data["card_order"].split(",")
        data = [d_data["slot1"], d_data["slot2"], d_data["slot3"], d_data["slot4"]]
        result = dict(zip(card_order, data))
        print("現在處理switch_csv", result)
        print("====================================")
        return result

    def get_pv_csv(self, d_data: dict):
        result = {"IP": d_data["ip"], "Gateway": d_data["gateway"]}
        print("現在處理pv_csv", result)
        print("====================================")
        return result

    def get_pms_csv(self, c_data: dict, d_data:dict, garage_code: str, customer_code: str, system_configuration: dict):
        result = {"Host": c_data["host"], "AcerStoreNo": garage_code, "customerCode": customer_code, "Position": d_data["driveway"],
            "API_url": system_configuration["API_config"]["API_url"], "API_port": system_configuration["API_config"]["API_port"], "API_account": system_configuration["API_config"]["API_account"], "API_psd": system_configuration["API_config"]["API_psd"]}
        print("現在處理pms_csv", result)
        print("====================================")
        return result

    def get_car_csv(self):
        result = {"CarNo": "        "}
        print("現在處理car_csv", result)
        print("====================================")
        return result

    def get_receipt_csv(self, g_data: dict, d_data: dict):
        result ={"Store_No": g_data["store_no"], "Pos_No": d_data["eid_pos_no"], "EID_Store_No": g_data["eid_store_no"]}
        print("現在處理receipt_csv", result)
        print("====================================")
        return result

    def get_server_csv(self, customer_code: str, garage_code: str, store_no: str, driveway: str, eid_pos_no: str, device_type: str, system_configuration: dict):
        instant_transaction_file = system_configuration["instant_transaction_file"]
        transaction_file = system_configuration["transaction_file"]
        eidc = system_configuration["eidc"]
        eid = system_configuration["eid"]
        device_monitor_file = system_configuration["device_monitor_file"]
        commutation_ticket = system_configuration["commutation_ticket"]
        black_list = system_configuration["black_list"]
        device_args = system_configuration["device_args"]
        API_config = system_configuration["API_config"]
        iBox_Ping = system_configuration["iBox_Ping"]
        pricing_rule = system_configuration["pricing_rule"]
        storage = system_configuration["storage"]

        # handle pms/ pms+ path
        # 現在暫時適用ftp
        InstantTransactionFile_Path = instant_transaction_file["project_path"] + "csvs/in/" + str(customer_code) + "/" + str(garage_code) + "/real_time_transaction/" + device_type + "/" if instant_transaction_file["ftp_mode"] == "ftps" else instant_transaction_file["project_path"] + "in/" + str(garage_code) + "/txn_data/"
        TransactionFile_Path = transaction_file["project_path"] + "csvs/in/" + str(customer_code) + "/" + str(garage_code) + "/transaction_files/" + device_type + "/" if transaction_file["ftp_mode"] == "ftps" else transaction_file["project_path"] + "in/" + str(garage_code) + "/transaction_files/"
        EIDC_Path = eidc["project_path"] + "csvs/in/" + str(customer_code) + "/" + str(garage_code) + "/einvoice/eidc" if eidc["ftp_mode"] == "ftps" else eidc["project_path"] + "in/" + str(garage_code) + "/EIDC/"
        EID_Path = eid["project_path"] + "csvs/in/" + str(customer_code) + "/" + str(garage_code) + "/einvoice/eid" if eid["ftp_mode"] == "ftps" else eid["project_path"] + "in/" + str(garage_code) + "/" + str(eid_pos_no)
        DeviceMonitorFile_Path = device_monitor_file["project_path"] + "csvs/in/" + str(customer_code) + "/" + str(garage_code) + "/monitorMessage/" if device_monitor_file["ftp_mode"] == "ftps" else device_monitor_file["project_path"] + "in/" + str(garage_code) + "/monitorMessage/"
        if black_list["ftp_mode"] == "ftps":
            BlackList_iCash = black_list["project_path"]+ "csvs/out/" + str(customer_code) + "/iCash.bl/"
            BlackList_iPass = black_list["project_path"]+ "csvs/out/" + str(customer_code) + "/iPass.bl/"
            BlackList_YHDP = black_list["project_path"]+ "csvs/out/" + str(customer_code) + "/happyCash.bl/"
            BlackList_ECC = black_list["project_path"]+ "csvs/out/" + str(customer_code) + "/ecc.bl/"
        else:
            BlackList_iCash = black_list["project_path"] + "out/iCash.bl/"
            BlackList_iPass = black_list["project_path"] + "out/iPass.bl/"
            BlackList_YHDP = black_list["project_path"] + "out/happyCash.bl/"
            BlackList_ECC = black_list["project_path"] + "out/ecc.bl/"

        result = {
        "InstantTransactionFile_IP": instant_transaction_file["ip"], "InstantTransactionFile_Port": instant_transaction_file["port"],
        "InstantTransactionFile_ftpMode": instant_transaction_file["ftp_mode"], "InstantTransactionFile_Account": instant_transaction_file["account"],
        "InstantTransactionFile_Psd": instant_transaction_file["password"],
        "InstantTransactionFile_Path": InstantTransactionFile_Path,
        "InstantTransactionFile_Schedule": instant_transaction_file["schedule"],

        "TransactionFile_IP": transaction_file["ip"], "TransactionFile_Port": transaction_file["port"],
        "TransactionFile_ftpMode": transaction_file["ftp_mode"], "TransactionFile_Account": transaction_file["account"],
        "TransactionFile_Psd": transaction_file["password"],
        "TransactionFile_Path": TransactionFile_Path,
        "TransactionFile_Schedule": transaction_file["schedule"],

        "EIDC_IP": eidc["ip"], "EIDC_Port": eidc["port"],
        "EIDC_ftpMode": eidc["ftp_mode"], "EIDC_Account": eidc["account"],
        "EIDC_Psd": eidc["password"],
        "EIDC_Path": EIDC_Path,
        "EIDC_Schedule": eidc["schedule"], "EIDC_Mode": eidc["eidc_mode"],

        "EID_IP": eid["ip"], "EID_Port": eid["port"],
        "EID_ftpMode": eid["ftp_mode"], "EID_Account": eid["account"],
        "EID_Psd": eid["password"],
        "EID_Path": EID_Path,
        "EID_Schedule": eid["schedule"], "EID_Mode": eid["eid_mode"],

        "DeviceMonitorFile_ip": device_monitor_file["ip"], "DeviceMonitorFile_port": device_monitor_file["port"],
        "DeviceMonitorFile_ftpMode": device_monitor_file["ftp_mode"], "DeviceMonitorFile_Account": device_monitor_file["account"],
        "DeviceMonitorFile_Psd": device_monitor_file["password"],
        "DeviceMonitorFile_Path": DeviceMonitorFile_Path,
        "DeviceMonitorFile_Schedule": device_monitor_file["schedule"],

        "CommutationTicketDat_ip": commutation_ticket["ip"], "CommutationTicketDat_Port": commutation_ticket["port"],
        "CommutationTicketDat_ftpMode": commutation_ticket["ftp_mode"], "CommutationTicketDat_Account": commutation_ticket["account"],
        "CommutationTicketDat_Psd": commutation_ticket["password"],
        "CommutationTicketDat_Path": commutation_ticket["project_path"] + "csvs/out/" + str(customer_code) + "/commutation_ticket/generate_dat/" + str(store_no) + "/",
        "CommutationTicketDat_Schedule": commutation_ticket["schedule"],

        "BlackList_ip": black_list["ip"], "BlackList_Port": black_list["port"],
        "BlackList_ftpMode": black_list["ftp_mode"], "BlackList_Account": black_list["account"],
        "BlackList_Psd": black_list["password"],
        "BlackList_iCash": BlackList_iCash,
        "BlackList_iPass": BlackList_iPass,
        "BlackList_YHDP": BlackList_YHDP,
        "BlackList_ECC": BlackList_ECC,
        "BlackList_Schedule": black_list["schedule"],

        "ImportDeviceArgs_IP": device_args["ip"], "ImportDeviceArgs_Port": device_args["port"],
        "ImportDeviceArgs_ftpMode": device_args["ftp_mode"], "ImportDeviceArgs_Account": device_args["account"],
        "ImportDeviceArgs_Psd": device_args["password"],
        "ImportDeviceArgs_Path": device_args["project_path"] + "csvs/out/" + str(customer_code) + "/" + str(garage_code) + "/" + str(driveway) + "/pv/",
        "ImportDeviceArgs_Schedule": device_args["schedule"],

        "iBox_Ping_IP": iBox_Ping["ip"], "iBox_Ping_Port": iBox_Ping["port"],
        "iBox_Ping_ftpMode": iBox_Ping["ftp_mode"], "iBox_Ping_Account": iBox_Ping["account"],
        "iBox_Ping_Psd": iBox_Ping["password"],
        "iBox_Ping_Path": iBox_Ping["project_path"],
        "iBox_Ping_Schedule": iBox_Ping["schedule"],

        "PricingRule_IP": pricing_rule["ip"], "PricingRule_Port": pricing_rule["port"],
        "PricingRule_ftpMode": pricing_rule["ftp_mode"], "PricingRule_Account": pricing_rule["account"],
        "PricingRule_Psd": pricing_rule["password"],
        "PricingRule_Path": pricing_rule["project_path"] + "csvs/out/" + str(customer_code) + "/" + str(garage_code) + "/" + str(driveway) + "/fee/",
        "PricingRule_Schedule": pricing_rule["schedule"],

        "Storage_IP": storage["ip"], "Storage_Port": storage["port"],
        "Storage_ftpMode": storage["ftp_mode"], "Storage_Account": storage["account"],
        "Storage_Psd": storage["password"],
        "Storage_Path": storage["project_path"],
        "Storage_Schedule": storage["schedule"],

        "API_url": API_config["API_url"], "API_port": API_config["API_port"],
        "API_account": API_config["API_account"], "API_Psd": API_config["API_psd"],

        "AcerStoreNo": garage_code, "customerCode": customer_code, "Position": driveway
        }
        print("現在處理server_csv")
        for i in result:
            print(str(i) + " : " + str(result[i]))
        return result

    # Service Part

    def get_service_ipass_csv(self, c_data: dict):
        if "ipass_water_lv_host" in c_data and "ipass_water_lv_port" in c_data:
            ipass_water_host = str(c_data["ipass_water_lv_host"]) + "," + str(c_data["ipass_water_lv_port"])
        else:
            ipass_water_host = " "
        result ={"iPass_Water_Host": ipass_water_host}
        print("現在處理service_ipass_csv", result)
        print("====================================")
        print(result)
        return result

    def get_service_pms_csv(self, c_data: dict):
        if "ipass_water_lv_port" in c_data:
            YHDP_water_lv_port = c_data["YHDP_water_lv_port"]
        else:
            YHDP_water_lv_port = " "
        if "ipass_water_lv_port" in c_data:
            ipass_water_lv_port = c_data["ipass_water_lv_port"]
        else:
            ipass_water_lv_port = " "
        result = {"PMS_Exchanger_Host": "Not_Use", "PMS_iPass_Listen_Port": ipass_water_lv_port,
        "PMS_YHDP_Listen_Port": YHDP_water_lv_port, "PMS_ECC_Listen_Port": "Not_Use"}
        print("現在處理service_pms_csv", result)
        print("====================================")
        return result
    
    def get_service_pv_csv(self, d_data: dict):
        result ={"Client_PV": d_data["client_pv"], "TimeSyncPeriod": d_data["time_sync_period"]}
        print("現在處理service_pv_csv", result)
        print("====================================")
        return result

    def get_service_YHDP_csv(self, c_data: dict):
        if "YHDP_water_lv_host" in c_data and "YHDP_water_lv_port" in c_data:
            YHDP_water_host = str(c_data["YHDP_water_lv_host"]) + "," + str(c_data["YHDP_water_lv_port"])
        else:
            YHDP_water_host = " "
        result ={"YHDP_Water_Host": YHDP_water_host}
        print("現在處理service_YHDP_csv", result)
        print("====================================")
        return result
        

# test
def main():
    a = {"fee_primary": {
            "fee_primary_table_id": 2,
            "fee_name": "台灣聯通瑞二場 機車費率",
            "introduction": "一次性付款 blah blah",
            "normal": "2018-07-03",
            "holiday": "2018-07-01",
            "update_time": "2018-08-30 17:38:56",
            "update_user": "root"
        },
        "normal_args": {
        "normal": {
            "cost_normal_rule_id": 3,
            "cost_normal_rule_day_type": 1,
            "mode": 1,
            "mode_method": "1",
            "mode_time": "00:00:00",
            "max_fee": "150",
            "max_fee_time": "24:00:00",
            "free_time": "00:00:00",
            "loop_mode": "0",
            "first_period_total": "01:00:00",
            "first_period": "01:00:00",
            "first_period_fee": "-1",
            "second_period_total": "00:00:00",
            "second_period": "00:00:00",
            "second_period_fee": "0",
            "third_period_total": "00:00:00",
            "third_period": "00:00:00",
            "third_period_fee": "0",
            "interval_1_fee_time_start": "08:00:00",
            "interval_1_fee_time_end": "17:00:00",
            "interval_1_period": "00:30:00",
            "interval_1_fee": "10",
            "interval_1_end_method": "1",
            "interval_2_fee_time_start": "17:00:00",
            "interval_2_fee_time_end": "08:00:00",
            "interval_2_period": "00:30:00",
            "interval_2_fee": "15",
            "interval_2_end_method": "1",
            "interval_3_other_period": "00:00:00",
            "interval_3_fee": "0",
            "interval_3_end_method": "1",
            "update_time": "2018-08-30 17:38:56",
            "update_user": "root",
            "fee_primary_table_id": "2"
        },
        "holiday": {
            "cost_normal_rule_id": 4,
            "cost_normal_rule_day_type": 2,
            "mode": 1,
            "mode_method": "1",
            "mode_time": "00:00:00",
            "max_fee": "300",
            "max_fee_time": "24:00:00",
            "free_time": "00:10:00",
            "loop_mode": "0",
            "first_period_total": "01:00:00",
            "first_period": "01:00:00",
            "first_period_fee": "-1",
            "second_period_total": "00:00:00",
            "second_period": "00:00:00",
            "second_period_fee": "30",
            "third_period_total": "00:00:00",
            "third_period": "00:00:00",
            "third_period_fee": "10",
            "interval_1_fee_time_start": "00:00:00",
            "interval_1_fee_time_end": "12:00:00",
            "interval_1_period": "00:30:00",
            "interval_1_fee": "5",
            "interval_1_end_method": "1",
            "interval_2_fee_time_start": "00:00:00",
            "interval_2_fee_time_end": "12:00:00",
            "interval_2_period": "00:30:00",
            "interval_2_fee": "5",
            "interval_2_end_method": "1",
            "interval_3_other_period": "00:30:00",
            "interval_3_fee": "20",
            "interval_3_end_method": "1",
            "update_time": "2018-08-30 17:38:56",
            "update_user": "root",
            "fee_primary_table_id": "2"
        }
        },
        "special_args": {
        "normal": {
            "cost_special_rule_id": 3,
            "cost_special_rule_day_type": 1,
            "on_off_1": 0,
            "mode_method_1": "1",
            "start_time_1": "01:00:00",
            "end_time_1": "12:00:00",
            "max_fee_1": "200",
            "free_time_1": "01:00:00",
            "first_period_total_1": "03:00:00",
            "first_period_1": "01:30:00",
            "first_period_fee_1": "50",
            "second_period_total_1": "00:00:00",
            "second_period_1": "00:00:00",
            "second_period_fee_1": "0",
            "third_period_total_1": "00:00:00",
            "third_period_1": "00:00:00",
            "third_period_fee_1": "0",
            "on_off_2": 0,
            "mode_method_2": "1",
            "start_time_2": "01:00:00",
            "end_time_2": "04:00:00",
            "max_fee_2": "200",
            "free_time_2": "00:00:00",
            "first_period_total_2": "03:00:00",
            "first_period_2": "01:30:00",
            "first_period_fee_2": "50",
            "second_period_total_2": "00:00:00",
            "second_period_2": "00:00:00",
            "second_period_fee_2": "0",
            "third_period_total_2": "00:00:00",
            "third_period_2": "00:00:00",
            "third_period_fee_2": "0",
            "update_time": "2018-08-30 17:38:56",
            "update_user": "root",
            "fee_primary_table_id": "2"
        },
        "holiday": {
            "cost_special_rule_id": 4,
            "cost_special_rule_day_type": 2,
            "on_off_1": 0,
            "mode_method_1": "1",
            "start_time_1": "01:00:00",
            "end_time_1": "04:00:00",
            "max_fee_1": "200",
            "free_time_1": "00:59:00",
            "first_period_total_1": "04:00:00",
            "first_period_1": "01:00:00",
            "first_period_fee_1": "50",
            "second_period_total_1": "00:00:00",
            "second_period_1": "00:00:00",
            "second_period_fee_1": "0",
            "third_period_total_1": "00:00:00",
            "third_period_1": "00:00:00",
            "third_period_fee_1": "0",
            "on_off_2": 0,
            "mode_method_2": "1",
            "start_time_2": "00:00:00",
            "end_time_2": "00:00:00",
            "max_fee_2": "200",
            "free_time_2": "00:00:00",
            "first_period_total_2": "03:00:00",
            "first_period_2": "01:30:00",
            "first_period_fee_2": "50",
            "second_period_total_2": "00:00:00",
            "second_period_2": "00:00:00",
            "second_period_fee_2": "0",
            "third_period_total_2": "00:00:00",
            "third_period_2": "00:00:00",
            "third_period_fee_2": "0",
            "update_time": "2018-08-30 17:38:56",
            "update_user": "root",
            "fee_primary_table_id": "2"
        }
        }
    }
    # print(a["fee_primary"])
    # q = CsvSpec()
    # q.get_full_fee_args_export_csv_data(a["fee_primary"], a["normal_args"], a["special_args"])

if __name__ == "__main__":
    main()
        
