import pprint
from datetime import datetime

class RealtimeParkingCompound(object):
    global device
    def __init__(self,transaction):
        self.parking = transaction
        self.real_time_transaction = transaction
    
    @property
    def parking (self):
        return self._parking
    
    # @property
    # def real_time_transaction (self):
    #     print(f'23332')
    #     return self._real_time_transaction
    
    @parking.setter
    def parking (self,transaction):
        #parking_columns=['id','pv','pv_out','card_id','card_id16','enter_time','exit_time','paid_time','duration','fee','real_fee','note','paid_type','entry_balance','exit_balance','settlement_type','txn_datetime','txn_amt','disability_mode','card_autoload_flag','entry_mode','last_source_filename','garage_code','last_csv_file_date','parking_id','create_date','vehicle_identification_number','modified_date','vehicle_type','enter_account_id','exit_account_id','einvoice','einvoice_print_status','record_status']
        keys = transaction.keys()
        dev_type = transaction['device_type']
        if dev_type == 3 or dev_type == 6:
            parking = self.parking_object(transaction['in_or_out'],transaction)
        elif dev_type == 30:
            parking = self.payagent_parking_object(transaction['in_or_out'], transaction)
        else:
            raise Exception(f'Not support device type for RealtimeParkingCompound(): {dev_type}')
        self._parking = parking
            
    # @real_time_transaction.setter
    # def real_time_transaction (self,transaction):
    #     real_time_transaction={}
    #     real_time_transaction_columns=['real_time_transaction_data_id','in_or_out','parking_type','card_id_16','in_or_out_datetime','pay_datetime','card_type','receivable','real_fees','before_pay_balance','is_disability','vehicle_identification_number','device_ip','garage_id','customer_id','discount_type','discount_amount','status_number','vehicle_type','einvoice','einvoice_print_status','tax_id_number','tax_id_number_buyer','card_id_appearance','is_autoload','autoload_amout','error_message','parking_id','create_account_id','create_date','exit_type_config_detail_id','exit_type_config_detail_remarks','ibox_no','record_status']
        
    #     for i in range(len(real_time_transaction_columns)):
    #         key = str(real_time_transaction_columns[i])
    #         if key in transaction:
    #             real_time_transaction[key] =transaction[key]
    #     self._real_time_transaction = real_time_transaction

    def parking_object(self, in_or_out, transaction):
        parking_object = {}
        if in_or_out == '0':
            #in
            parking_object['fee'] =transaction['receivable']
            parking_object['paid_type'] =transaction['card_type']
            parking_object['real_fee'] = transaction['real_fees']
            parking_object['entry_balance'] = transaction['before_pay_balance']
            parking_object['exit_balance'] ='0'
            parking_object['settlement_type'] = '0'
            parking_object['txn_amt'] = transaction['real_fees']
            parking_object['duration'] = 0
            parking_object['entry_mode'] = 1
            parking_object['pv'] = '進場'
            parking_object['pv_out'] = '出場'
            parking_object['garage_id'] = transaction['garage_id']
            parking_object['card_id16'] = transaction['card_id_16']
            parking_object['card_id'] = transaction.get('card_id_appearance', None)
            parking_object['enter_time'] = transaction['in_or_out_datetime']
            parking_object['exit_time'] = '0000-00-00 00:00:00'
            parking_object['paid_time'] = '0000-00-00 00:00:00'
            parking_object['txn_datetime'] = '0000-00-00 00:00:00'
            parking_object['card_autoload_flag'] = transaction['is_autoload']
            parking_object['vehicle_identification_number'] = transaction['vehicle_identification_number']
            parking_object['disability_mode'] = transaction['is_disability']
            parking_object['vehicle_type'] = transaction.get('vehicle_type', None)
            parking_object['garage_code'] = transaction['garage_code']
            parking_object['create_date'] = datetime.utcnow()
            parking_object['discount_type'] = transaction.get('discount_type', None)
            parking_object['discount_amount'] = transaction.get('discount_amount', None)
            parking_object['pklot_order_id'] = transaction.get('pklot_order_id', None)
            parking_object['pklot_member'] = transaction.get('pklot_member', None)
            parking_object['in_device_type'] = transaction['device_type']
            parking_object['commutation_ticket_config_id'] = transaction.get('parking_type', None)
            parking_object['in_device_id'] = transaction.get('device_id', None)
            parking_object['record_status'] = transaction.get('record_status', '1')
            parking_object['parking_space_no'] = transaction.get('parking_space_no', None)

        elif in_or_out == '1':
            #out
            parking_object['parking_id']= transaction['parking_id']
            parking_object['fee']= transaction['receivable']
            parking_object['txn_amt'] = transaction['real_fees']
            parking_object['card_autoload_flag'] = transaction['is_autoload']
            parking_object['real_fee'] = transaction['real_fees']
            parking_object['exit_time'] = transaction['in_or_out_datetime']
            parking_object['paid_time'] = transaction.get('pay_datetime', '0000-00-00 00:00:00')
            parking_object['garage_id'] = transaction['garage_id']
            parking_object['txn_datetime'] = transaction.get('pay_datetime', '0000-00-00 00:00:00')
            parking_object['tax_buyer_id'] = transaction.get('tax_id_number_buyer', None)
            parking_object['out_device_type'] = transaction['device_type']
            parking_object['commutation_ticket_config_id'] = transaction.get('parking_type', None)
            parking_object['out_device_id'] = transaction.get('device_id', None)
            parking_object['record_status'] = transaction.get('record_status', '1')
            parking_object['paid_type'] = transaction.get('card_type', None)
            parking_object['parking_space_no'] = transaction.get('parking_space_no', None)

        parking_object['is_urgent_handle'] = 0
        return parking_object

    def payagent_parking_object(self,in_or_out,transaction):
        parking_object = {}
        if in_or_out == '0':
            #in
            parking_object['fee'] =transaction['receivable']
            parking_object['paid_type'] =transaction['card_type']
            parking_object['real_fee'] = transaction['real_fees']
            parking_object['entry_balance'] = transaction['before_pay_balance']
            parking_object['exit_balance'] ='0'
            parking_object['settlement_type'] = '0'
            parking_object['txn_amt'] = transaction['real_fees']
            parking_object['duration'] = 0
            parking_object['entry_mode'] = 1
            parking_object['pv'] = ''
            parking_object['pv_out'] = ''
            parking_object['garage_id'] = transaction['garage_id']
            parking_object['card_id16'] = transaction['card_id_16']
            parking_object['card_id'] = transaction['card_id_appearance']
            parking_object['enter_time'] = transaction['in_or_out_datetime']
            parking_object['exit_time'] = '0000-00-00 00:00:00'
            parking_object['paid_time'] = '0000-00-00 00:00:00'
            parking_object['txn_datetime'] = '0000-00-00 00:00:00'
            parking_object['card_autoload_flag'] = transaction['is_autoload']
            parking_object['vehicle_identification_number'] = transaction['vehicle_identification_number']
            parking_object['disability_mode'] = transaction['is_disability']
            parking_object['vehicle_type'] = transaction['vehicle_type']
            parking_object['garage_code'] = transaction['garage_code']
            parking_object['create_date'] = datetime.utcnow()
            parking_object['discount_type'] = transaction['discount_type']
            parking_object['discount_amount'] = transaction['discount_amount']
            parking_object['pklot_order_id'] = transaction.get('pklot_order_id', None)
            parking_object['pklot_member'] = transaction.get('pklot_member', None)
            parking_object['in_device_type'] = transaction['device_type']

            parking_object['note'] = ''
            if 'record_status' in transaction :
                parking_object['record_status'] = transaction['record_status']

        elif in_or_out == '1':
            #out
            parking_object['parking_id']= transaction['parking_id']
            parking_object['fee']= transaction['receivable']
            parking_object['txn_amt'] = transaction['real_fees']
            parking_object['card_autoload_flag'] = transaction['is_autoload']
            parking_object['real_fee'] = transaction['real_fees']
            parking_object['exit_time'] = transaction['in_or_out_datetime']
            parking_object['paid_time'] = transaction['pay_datetime']
            parking_object['garage_id'] = transaction['garage_id']
            parking_object['txn_datetime'] = transaction['pay_datetime']
            parking_object['tax_buyer_id'] = transaction.get('tax_id_number_buyer', None)
            parking_object['out_device_type'] = transaction['device_type']

            if transaction.get('card_type', None) is not None:
                parking_object['paid_type'] = transaction['card_type']

            parking_object['record_status'] = transaction.get('record_status', None)

            only_for_parking = transaction['only_for_parking']
            parking_object['pv'] = only_for_parking['device_name']
            parking_object['pv_out'] = only_for_parking['device_name']
            parking_object['vp_deduct_point'] = only_for_parking['vp_deduct_point']
            parking_object['vp_deduct_from'] = only_for_parking['vp_deduct_from']
            parking_object['vp_deduct_rule'] = only_for_parking['vp_deduct_rule']


        return parking_object





        
            
        
        
