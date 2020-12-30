import pprint
from datetime import datetime

class GarageCapacity(object):
    #  await conn.execute(''' ALTER TABLE garage ADD COLUMN current_capacity_sedan int COMMENT '汽車剩餘車道' ''')
    #         await conn.execute(''' ALTER TABLE garage ADD COLUMN current_capacity_suv int COMMENT 'UV剩餘車道' ''')
    #         await conn.execute(''' ALTER TABLE garage ADD COLUMN current_capacity_bicycle int COMMENT '腳踏車剩餘車道' ''')
    #         await conn.execute(''' ALTER TABLE garage ADD COLUMN current_capacity_motocycle int COMMENT '機車剩餘車道' ''')
    #         await conn.execute(''' ALTER TABLE garage ADD COLUMN current_capacity_truck int COMMENT '卡車剩餘車道' ''')
    #         await conn.execute(''' ALTER TABLE garage ADD COLUMN current_capacity_bus int COMMENT '客運剩餘車道' ''')
    #         await conn.execute(''' ALTER TABLE garage ADD COLUMN current_capacity_total int COMMENT '總剩餘車道' ''')
    #         await conn.execute(''' ALTER TABLE garage ADD COLUMN current_capacity_updatetime timestamp COMMENT '更新日期' ''')
    #         await conn.execute(''' ALTER TABLE garage ADD COLUMN gov_id id COMMENT '政府id' ''')
    
    def __init__(self, current_capacity_sedan, current_capacity_suv, current_capacity_bicycle, current_capacity_motocycle
        , current_capacity_truck, current_capacity_bus, current_capacity_total, gov_id, current_capacity_updatetime):
        self.current_capacity_sedan = current_capacity_sedan
        self.current_capacity_suv = current_capacity_suv
        self.current_capacity_bicycle = current_capacity_bicycle
        self.current_capacity_motocycle = current_capacity_motocycle
        self.current_capacity_truck = current_capacity_truck
        self.current_capacity_bus = current_capacity_bus
        self.current_capacity_total = current_capacity_total
        self.gov_id = gov_id
        self.current_capacity_updatetime = current_capacity_updatetime
    
    @property
    def cur (self):
        return self._parking
    
    # @property
    # def real_time_transaction (self):
    #     print(f'23332')
    #     return self._real_time_transaction
    
    @parking.setter
    def parking (self,transaction):
        #parking_columns=['id','pv','pv_out','card_id','card_id16','enter_time','exit_time','paid_time','duration','fee','real_fee','note','paid_type','entry_balance','exit_balance','settlement_type','txn_datetime','txn_amt','disability_mode','card_autoload_flag','entry_mode','last_source_filename','garage_code','last_csv_file_date','parking_id','create_date','vehicle_identification_number','modified_date','vehicle_type','enter_account_id','exit_account_id','einvoice','einvoice_print_status','record_status']
        keys = transaction.keys()
        if transaction['device_type'] == 3:
            for k in range(len(keys)):
                parking = self.parking_object(transaction['in_or_out'],transaction)
        self._parking = parking
            
   



        
            
        
        
