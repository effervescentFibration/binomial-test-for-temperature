import csv
from scipy.stats import binom_test

months = dict()

higher_days = 0
lower_days = 0
t_old = 0.0

with open("./1914185.csv", "r") as f:
    data = csv.reader(f, delimiter=',', quotechar='"')
    i = 0
    for line in data:
        if not i or i == len(line):
            i += 1
            continue
        date = line[2]
        t_min = line[3]
        t_max = line[4]
        t_obs = line[5]
        # use the observed temperature
        t = t_max
        # first date for which full data exists is 1952-06-01
        year, month, day = date.split("-")
        year  = int(year)
        month = int(month)
        day   = int(day)
        if month not in months.keys():
            months[month] = []
        if year >= 1952:
            year_offset = year - 1952
            while year_offset >= len(months[month]):
                months[month].append([])
            if t:
                months[month][year_offset].append(float(t))

                if t_old:
                    if t_old > t:
                        lower_days += 1
                    if t > t_old:
                        higher_days += 1
                t_old = t
        i += 1

month_averages = dict()
higher_years = 0
lower_years = 0
for month, years in months.items():
    j = 0
    old_avg = 0.0
    for year in years:
        avg = 0.0
        i = 0
        for day in year:
            if day:
                avg += day
                i += 1
                avg /= float(i)
        print(
            "Average temp in month " +
            str(month) +
            " for year " +
            str(j + 1952) +
            str(":") +
            str(avg)
        )
        if avg > 0.0:
            if old_avg > 0.0:
                if avg > old_avg:
                    higher_years += 1
                elif avg < old_avg:
                    lower_years += 1
            old_avg = avg
        j += 1
x = [higher_days, lower_days]
print(repr(x))
print("Test result is " + str(binom_test(x, p=0.5, alternative="greater")))
