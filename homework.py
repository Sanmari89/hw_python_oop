import datetime as dt
DATE_FORMAT = '%d.%m.%Y'


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_week_stats(self):
        today = dt.datetime.now().date()
        that_week = today - dt.timedelta(weeks=1)
        result = 0
        for record in self.records:
            if that_week <= record.date <= today:
                result += record.amount
        return result

    def get_today_stats(self):
        count = 0
        today = dt.datetime.now().date()
        for record in self.records:
            if record.date == today:
                count += record.amount
        return count

    def get_diff(self):
        return self.limit - self.get_today_stats()


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, DATE_FORMAT).date()


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        today_diff = self.get_diff()
        if self.get_diff() <= 0:
            return 'Хватит есть!'

        return ('Сегодня можно съесть что-нибудь ещё, '
                f'но с общей калорийностью не более {today_diff} кКал')


class CashCalculator(Calculator):
    USD_RATE = 76.0
    EURO_RATE = 91.0

    def get_today_cash_remained(self, currency):
        diff = self.get_diff()

        if diff == 0:
            return 'Денег нет, держись'

        currency_dict = {'usd': (self.USD_RATE, 'USD'),
                         'eur': (self.EURO_RATE, 'Euro'),
                         'rub': (1, 'руб')}

        value = abs(round(diff / currency_dict[currency][0], 2))
        currency = currency_dict[currency][1]

        if diff > 0:
            return f'На сегодня осталось {value} {currency}'

        return (f'Денег нет, держись: твой долг - {value} '
                f'{currency}')
