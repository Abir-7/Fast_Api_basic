from datetime import datetime,timedelta,timezone

def gen_exp_time(number:int):
    expire_time = datetime.now() + timedelta(minutes=number)
    return expire_time 
    