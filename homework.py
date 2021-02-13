from datetime import datetime as dt
from datetime import timedelta as td


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def sum_records(self):
        result = 0
        for record in self.records:
            result += record.amount
        return result

    def dates_records(self, date_list):
        result = 0
        for record in self.records:
            if record.date in date_list:
                result += record.amount
        return result

    def get_week_stats(self):
        today = dt.now().date()
        date_list = [today - td(days=x) for x in range(7)]
        return self.dates_records(date_list)

    def get_today_stats(self):
        count = 0
        today = dt.now().date()
        for record in self.records:
            if record.date == today:
                count += record.amount
        return count


class Record:
    def __init__(self, amount, comment, date=dt.now().date()):
        date_format = '%d.%m.%Y'
        if type(date) == str:
            date = dt.strptime(date,date_format).date()
        self.amount = amount
        self.comment = comment
        self.date = date


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        count_calories = 0
        result = f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {self.limit} кКал'
        for record in self.records:
            today = dt.now().date()
            if record.date == today:
                count_calories += record.amount
                if count_calories < self.limit:
                    N = self.limit - count_calories
                    result = f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {N} кКал'
                else:
                    result = 'Хватит есть!'
        return result


class CashCalculator(Calculator):
    USD_RATE = 76.0
    EURO_RATE = 91.0

    def get_today_cash_remained(self, currency):
        currency_dict = {'usd': (CashCalculator.USD_RATE, 'USD'),
                         'eur': (CashCalculator.EURO_RATE, 'Euro'),
                         'rub': (1, 'руб')}

        dif = self.limit - self.get_today_stats()
        value = round(dif / currency_dict[currency][0], 2)

        if dif == 0:
                return 'Денег нет, держись'

        if self.limit > self.get_today_stats():
            return f'На сегодня осталось {value} {currency_dict[currency][1]}'
        else:
            return f'Денег нет, держись: твой долг - {abs(value)} {currency_dict[currency][1]}'
