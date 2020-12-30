# import requests

# header = {"Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MiwidGVzdCI6InRlc3QiLCJleHAiOjE1ODMxOTYzMTl9.kBP_506oS0m5xeNXWg04iKevhydVhVglgYWPB5gMYVY"}
# # a = requests.get('http://192.168.190.1:8000/api/v1/accounts',headers= header)
# a = requests.get('http://192.168.0.102:8081/query_usb')
# # print(type(a))
# # print(a.url)
# # print(a.text)

# # data = {"iBox": {"store_no": "ggggg", "garage_id": 1, "garage_ibox_args_id": 1}, "device_type": "iBox", "garage": {"garage_code":"kkkk"}}

# data = {"setting": {"Date": "2018-01-17 00:00:00", "Station_InOut": "1", "Printer": "0", "Store_No": "323", "Pos_No": "001", "Tax_ID_Num": "86517413", "NTP_Server": "103.18.128.60"}, "switch": {"ECC": "1", "iPass": "1", "iCash": "0", "YHDP": "1"}, "PV": {"IP": "192.168.198.201", "Gateway": "192.168.198.254"}}
# c = requests.post('http://192.168.0.102:8081/query_usb', json=data)
# # c = requests.post('http://192.168.190.1:8000/api/v1/garage', json=data, headers = header)
# print(c.url)
# print(c.text)

# import time
# datetime_format = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
# with open("./version.txt", "a") as f:
#     version_message = str(datetime_format) + " db schema version : " + "V1.5"
#     f.write(version_message + "\n")
# f.close()

# python內 使用 command
# import subprocess
# subprocess.run(["mkdir", "abcde"])

# CREATE OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `device_view` AS 
# '''
# select from device_ibox_args
# '''

a = [{"fee":10, "cnt": 2, "subtotal": 20}, {"fee":20, "cnt": 3, "subtotal": 40}, {"fee":50, "cnt": 4, "subtotal": 100}]

fee = []
fee_cnt = []
subtotal = []
for i in range(0, 115, 5):
    flag = True
    for j in a:
        if i == j['fee']:
            fee_cnt.append(j['cnt'])
            subtotal.append(j['subtotal'])
            flag = False
    if flag:
        fee_cnt.append(0)
        subtotal.append(0)

print(fee_cnt)
print(len(fee_cnt))

print(subtotal)
print(len(subtotal))
        
# print(x)

# c = [{"fee":1},2,3]
# print(11 in c)