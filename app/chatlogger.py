from datetime import datetime

DELIMITER = "|"

def timestamp(as_int=False):
    if not as_int:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        return int(datetime.now().timestamp())

def log(userid, timestamp, role, content):
    print(f"{userid}{DELIMITER}{timestamp}{DELIMITER}{role}{DELIMITER}{content}")
