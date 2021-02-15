import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_week_stats(self):
        today = dt.datetime.now().date()
        result = 0
        for record in self.records:
            if today - dt.timedelta(weeks=1) <= record.date <= today:
                result += record.amount
        return result

    def get_today_stats(self):
        count = 0
        today = dt.datetime.now().date()
        for record in self.records:
            if record.date == today:
                count += record.amount
        return count

    def diff(self, today_stats):
        return self.limit - today_stats


class Record:
    date_format = '%d.%m.%Y'

    def __init__(self, amount, comment, date=None):
        if date is None:
            date = dt.datetime.now().date()
        else:
            date = dt.datetime.strptime(date, Record.date_format).date()
        self.amount = amount
        self.comment = comment
        self.date = date


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        today_stats = self.get_today_stats()
        if self.limit <= today_stats:
            return 'Хватит есть!'

        diff = self.diff(today_stats)

        if diff > 0:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {diff} кКал')


class CashCalculator(Calculator):
    USD_RATE = 76.0
    EURO_RATE = 91.0

    def get_today_cash_remained(self, currency):
        today_stats = self.get_today_stats()

        if self.limit == today_stats:
            return 'Денег нет, держись'

        currency_dict = {'usd': (CashCalculator.USD_RATE, 'USD'),
                         'eur': (CashCalculator.EURO_RATE, 'Euro'),
                         'rub': (1, 'руб')}

        diff = self.diff(today_stats)
        value = abs(round(diff / currency_dict[currency][0], 2))
        currency = currency_dict[currency][1]

        if diff > 0:
            return f'На сегодня осталось {value} {currency}'

        return (f'Денег нет, держись: твой долг - {value} '
                    f'{currency}')
