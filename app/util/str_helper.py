
import datetime

class StringHelper(object):
    
    @staticmethod
    def date_str_to_timestamp(date: str, f: str = "%Y-%m-%d %H:%M:%S", date_str_timezone='TW'):
        dt = datetime.datetime.strptime(date, f)

        # replace timezone to utc �O�]��server�W���ɰϳ]�w���i��|��
        # �p�G�S�]�ɰϡAtimestamp�N�|��server�W�]�w���ɰϰ�timestamp���ഫ
        # �ҥH��timestamp�e�n�Τ@�ରutc�ɰϦA�h����
        return StringHelper.datetime_to_timestamp(dt, date_str_timezone)

    @staticmethod
    def datetime_to_timestamp(tw_datetime,  datetime_timezone='TW'):
        if datetime_timezone.upper() == 'UTC':
            timezone_diff = 0
        elif datetime_timezone.upper() == 'TW':
            timezone_diff = -28800
        else:
            raise RuntimeError('Not support datetime timezone')

        # replace timezone to utc �O�]��server�W���ɰϳ]�w���i��|��
        # �p�G�S�]�ɰϡAtimestamp�N�|��server�W�]�w���ɰϰ�timestamp���ഫ
        # �ҥH��timestamp�e�n�Τ@�ରutc�ɰϦA�h����
        return int(tw_datetime.replace(tzinfo=datetime.timezone.utc).timestamp() + timezone_diff)
