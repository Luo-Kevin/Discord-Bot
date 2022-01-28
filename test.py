import datetime as dt

def time():
    now = dt.datetime.now(dt.timezone.utc)
    todayUTC = now.replace(hour=16, minute=0, second=0, microsecond=1)
    if now > todayUTC:
        date = dt.date.today()
        return date
    else:
        today = dt.date.today()
        yesterday = today - dt.timedelta(days=1)
        return yesterday


TIME = time()
print(time)