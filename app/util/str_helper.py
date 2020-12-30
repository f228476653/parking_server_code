
import datetime

class StringHelper(object):
    
    @staticmethod
    def date_str_to_timestamp(date: str, f: str = "%Y-%m-%d %H:%M:%S", date_str_timezone='TW'):
        dt = datetime.datetime.strptime(date, f)

        # replace timezone to utc 是因為server上的時區設定有可能會變
        # 如果沒設時區，timestamp就會用server上設定的時區做timestamp的轉換
        # 所以拿timestamp前要統一轉為utc時區再去換算
        return StringHelper.datetime_to_timestamp(dt, date_str_timezone)

    @staticmethod
    def datetime_to_timestamp(tw_datetime,  datetime_timezone='TW'):
        if datetime_timezone.upper() == 'UTC':
            timezone_diff = 0
        elif datetime_timezone.upper() == 'TW':
            timezone_diff = -28800
        else:
            raise RuntimeError('Not support datetime timezone')

        # replace timezone to utc 是因為server上的時區設定有可能會變
        # 如果沒設時區，timestamp就會用server上設定的時區做timestamp的轉換
        # 所以拿timestamp前要統一轉為utc時區再去換算
        return int(tw_datetime.replace(tzinfo=datetime.timezone.utc).timestamp() + timezone_diff)
