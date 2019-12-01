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


def monthly_income(salary, rent, expense, future_months,payday):
    y,m,d = int(payday.split('-')[0]),int(payday.split('-')[1]),int(payday.split('-')[2])

    paydays = get_pay_days(d, m, y)

    month_year = [day.strftime('%Y/%m') for day in paydays]

    freq = {}
    for item in month_year:
        freq[item] = month_year.count(item)

    month_year_list = sorted(list(set(month_year)))[0:future_months]

    month_pay_data = []
    for month in month_year_list:

        num_pay_days = freq[month]
        print('%s has %s paydays' % (str(month), str(num_pay_days)))

        income = num_pay_days * salary
        print('Post tax income: %s' % str(income))

        net = income - rent - expense
        print('net income of: %s' % str(net))

        month_pay = {'month':month,'num_pay_days':num_pay_days , 'income':income, 'net':net,'rent':rent,'expense':expense}
        month_pay_data.append(month_pay)
        print('\n')

    return month_pay_data


def project_future(monthly_pay_data, debt, debt_payoff_rate, asset, asset_growth_rate):
    """ project future income based on paying off debt and saving

    :param monthly_pay_data: list of dictionaries on monthly income
    :param debt: total debt
    :param debt_payoff_rate: % of remaining income going to paying off debt
    :param asset: total assets
    :param asset_growth_rate: expected monthly % growth rate for assets (default .07/12)
    :return: list of dictionaries of monthly projection info
    """
    project_month_data = []

    asset_increase = 0
    for month in monthly_pay_data:
        savings = 0
        debt_payment = round(month['net'] * debt_payoff_rate,2)
        debt = round(debt - debt_payment,2)

        if debt < 0:
            savings = abs(debt)
            debt = 0

        savings = round(month['net'] * (1 - debt_payoff_rate),2)

        #new_asset = round(asset * (1 + asset_growth_rate),2)
        increase = round((asset * asset_growth_rate), 2)
        asset_increase += increase
        projected_asset = round(asset + asset_increase,2)

        net_worth = round(calculate_networth(projected_asset,debt),2)

        projection = {'month':month['month'],'net':month['net'],'debt':debt,'debt_payment':debt_payment,'savings':savings,
                      'assets':projected_asset,'net_worth':net_worth}

        project_month_data.append(projection)

    return project_month_data


def calculate_networth(assets,debt):
    net = assets - debt

    return net


salary = data['salary']
rent = data['rent']
expense = data['expense']
debt = data['debt']
assets = data['asset']
future_months = 12
payday = '2019-11-1' # any previous payday
month_pay_data = monthly_income(salary,rent,expense, future_months,payday)


future = project_future(month_pay_data,debt,.6,assets,.006)
print(future)

for f in future:
    print(f)


