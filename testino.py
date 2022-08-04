from datetime import datetime 
from website.models import toWeekDay

print(toWeekDay(datetime.now().weekday()))