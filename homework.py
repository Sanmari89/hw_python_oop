import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_week_stats(self):
        today = dt.datetime.now().date()
        date_list = [today - dt.timedelta(days=x) for x in range(7)]
        result = 0
        for record in self.records:
            for date in date_list:
                if record.date == date:
                    result += record.amount
        return result

    def get_today_stats(self):
        count = 0
        today = dt.datetime.now().date()
        for record in self.records:
            if record.date == today:
                count += record.amount
        return count


class Record:
    def __init__(self, amount, comment, date=''):
        date_format = '%d.%m.%Y'
        if date == '':
            date = dt.datetime.now().date()
        if type(date) == str:
            date = dt.datetime.strptime(date, date_format).date()
        self.amount = amount
        self.comment = comment
        self.date = date


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        if self.limit <= self.get_today_stats():
            return 'Хватит есть!'

        diff = self.limit - self.get_today_stats()

        if diff > 0:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {diff} кКал')


class CashCalculator(Calculator):
    USD_RATE = 76.0
    EURO_RATE = 91.0

    def get_today_cash_remained(self, currency):
        currency_dict = {'usd': (CashCalculator.USD_RATE, 'USD'),
                         'eur': (CashCalculator.EURO_RATE, 'Euro'),
                         'rub': (1, 'руб')}

        if self.limit == self.get_today_stats():
            return 'Денег нет, держись'

        diff = self.limit - self.get_today_stats()
        value = abs(round(diff / currency_dict[currency][0], 2))

        if diff > 0:
            return f'На сегодня осталось {value} {currency_dict[currency][1]}'
        else:
            return (f'Денег нет, держись: твой долг - {value} '
                    f'{currency_dict[currency][1]}')
