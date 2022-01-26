import datetime as dt


class Record:
    # Можно в инит дефолтное значение date сразу определить 
    # 'dt.datetime.now().strftime('%d.%m.%Y')', а не просто пустой строкой.
    # тогда в self.date написать 'dt.datetime.strptime(date, '%d.%m.%Y').date()',
    # таким образом код станет более читаемым и избегаем длинных строк.

    def __init__(self, amount, comment, date=''):
        self.amount = amount
        #Не самые лучшие переносы. Так более читаемо.
        self.date = (
            dt.datetime.now().date() if not date else dt.datetime.strptime(
                date, '%d.%m.%Y'
                ).date()
                )
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        '''
        Хорошая практика, оставлять описание функции в таком виде,
        в трех ковчках в нутки функции
        '''
        x = self.limit - self.get_today_stats()
        if x > 0:
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал' 
        else:
            return('Хватит есть!')


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    # Опять перносы. Плохие переносы ухудшат читаемость
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
    # def get_today_cash_remained(
    #     self, currency,USD_RATE=USD_RATE, EURO_RATE=EURO_RATE
    #     ): так лучше
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        # Плодить if не самая лучшая идея. В этом случае лучше воспользоваться 
        # соварем (dict). В таком случае курс-валюты (key),
        # математическое действие (value)
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            cash_remained == 1.00
            currency_type = 'руб'
        if cash_remained > 0:
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)
            # return 'Денег нет, держись: твой долг - {0:.2f} {1}'.format(
            #            -cash_remained, currency_type
            #            )  Опять же так лучше

    def get_week_stats(self):
        super().get_week_stats()


cash_calculator = CashCalculator(1000)
сalories_calculator = CaloriesCalculator(1000)
сalories_calculator.add_record(Record(amount=1450, comment="кофе"))
cash_calculator.add_record(Record(amount=145, comment="кофе"))
cash_calculator.add_record(Record(amount=300, comment="обед"))
cash_calculator.add_record(Record(amount=3000, comment="ужин", date="08.11.2019"))
print(cash_calculator.get_today_cash_remained("rub"))
print(сalories_calculator.get_calories_remained())