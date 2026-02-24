# A date in Python is not a data type of its own, but we can import a module named datetime to work with dates as date objects.
#1 Import the datetime module and display the current date:
import datetime

x = datetime.datetime.now()
print(x)

#2 Return the year and name of weekday:
import datetime

x = datetime.datetime.now()

print(x.year)
print(x.strftime("%A"))

#3 Create a date object:
import datetime

x = datetime.datetime(2020, 5, 17)

print(x)

#4Display the name of the month:
import datetime

x = datetime.datetime(2018, 6, 1)

print(x.strftime("%B"))

#5 Convert String to Date
from datetime import datetime

date_string = "16-02-2026"
dt = datetime.strptime(date_string, "%d-%m-%Y")
print(dt)