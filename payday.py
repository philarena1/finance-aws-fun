from datetime import date, timedelta
from personal import data


def pay_day(day,month,year):
    d = date(year,month,day)
    d += timedelta(days = 4 - d.weekday())
    while d.year < year + 2:
        yield d
        d += timedelta(days = 14)

def get_pay_days(day,month,year):
    pay_days = []
    for d in pay_day(day,month,year):
        pay_days.append(d)

    return pay_days

paydays = get_pay_days(1,11,2019) # input a day you got paid

curr_mon, curr_year = date.today().month, date.today().year

month_year = [day.strftime('%Y/%m') for day in paydays]

freq = {}
for item in month_year:
    freq[item] = month_year.count(item)

num_pay_days = (freq[(str(curr_year)+'/'+str(curr_mon))])



salary = data['salary']
rent = data['rent']
expense = data['expense']


# how many months to look
future_months = 6

month_year_list = sorted(list(set(month_year)))[0:future_months]

for month in month_year_list:
    num_pay_days = freq[month]
    print('%s has %s paydays' % (str(month), str(num_pay_days)))

    income = num_pay_days * salary
    print('Post tax income: %s' % str(income))

    net = income - rent - expense
    print('net income of: %s' % str(net))

    print('\n')
