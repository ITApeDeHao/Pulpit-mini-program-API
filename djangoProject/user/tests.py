
from django.test import TestCase
import time
# Create your tests here.

dt = "2023-03-28 16:00"

#转换成时间数组
timeArray = time.strptime(dt, "%Y-%m-%d %H:%M")
#转换成时间戳
timestamp = time.mktime(timeArray)
print(timestamp)