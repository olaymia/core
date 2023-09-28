from datetime import datetime    
from django.utils import timezone
import pytz    

def get_local_time():
    tz_NY = pytz.timezone('Asia/Kolkata')   
    datetime_NY = datetime.now(tz_NY)  
    return datetime_NY.strftime("%Y-%m-%d %H:%M:%S")



def get_datetime(date=timezone.now()):
    
    import pytz   
    timezone = pytz.timezone('Asia/Kolkata')
    return date.astimezone(timezone)