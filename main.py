import datetime as dt


class Record:
    # значение по умолчанию правильнее определить через None
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        """
        Можно записать компактнее используя dt.date.today() и "перевернув" сравнение убрав not
        self.date = (
            dt.datetime.strptime(date, '%d.%m.%Y').date() if date
            else dt.date.today()
        )
        """
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        """
        Имена переменных следует задавать в нижнем регистре, в текущем случае переменная Record совпадает с классом Record
        
        Сам метод можно сделать компактнее используя операторы filter для получения списка записей подходящих по дате
        сформировать список из значений полей amount выбранных объектов
        и с помощью оператора sum получить сумму
        """
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                # Лучше использовать оператор +=
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        # Можно использовать dt.date.today()
        today = dt.datetime.now().date()
        for record in self.records:
            """
            Тут лучше использовать цепочку сравнения, это сделает код более компактным и читаемым,
            так же это сократит использование переменной today до одного раза, в связи с чем можно будет ее упразднить
            и использовать dt.datetime.now().date() в сравнении, длина строки позволяет это сделать.
            """
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats
 
class CaloriesCalculator(Calculator):
    # Комментарии к методам лучше размещать перед самим методом.
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        # Вместо 'x' лучшее использовать более понятное название переменной, которое будет отражать ее назначение
        x = self.limit - self.get_today_stats()
        if x > 0:
            # Для переноса строк код необходимо использовать () вместо бэкслэша \
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        # Оператор else в данном случае не требуется так как этот код итак отработает только в случае невыполнения условия x > 0
        else:
            return('Хватит есть!')


class CashCalculator(Calculator):
    """
    Для этих констант комментарии не требуются поскольку наименование констант отражает их назначение (комментарии являются просто переводом)
    
    Вызов метода float не требуется, это лишнее действие для конвертации int -> float, можно сразу задать значение константы 
    как float, то есть в формате 60.0
    
    Есть сомнения в целесообразности хранения курсов валют таким образом, более детально в комментариях к методу get_today_cash_remained
    """
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    # Согласно заданию данный метод должен получать только currency, возможность указания рейтов не требуется.
    # Но если добавлять такой функционал то через одну переменную rate, иначе это будет сложно маштабировать при добавлении новой валюты
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        # В новой переменной нет необходимости 
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        """
        Данную логику можно оптимизировать, сделать более маштабируемой и понятной
        Например для хранения курсов валют использовать не константы с курсами (USD_RATE, EURO_RATE) 
        а dict() который будет содержать ключи (usd, eur, rub ...) 
        и все характеристики каждой валюты, курс относительно рубля, отображаемое имя и так далее.
        
        Это так же будет удобно при дальнейшем развитии проекта если потребуется подключить внешний источник данных с курсами валют.
        
        А громоздкую if/elif/else констуркцию можно будет заменить на: cash_remained /= self.CURRENCIES[currency]['rate']
        обращаясь таким образом к любой требуемой характеристике валюты.
        
        Так же следует добавить обработку кейса когда нам передали валюту которой нет
        """
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # В этой строке мы просто возвращаем булевое значение которое нигде не используется, можно убрать
            cash_remained == 1.00
            currency_type = 'руб'
        # Тут можно разделить логические блоки пустой строкой
        if cash_remained > 0:
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        # Вместо последнего elif лучше использовать else это будет подразумевать все остальные случаи
        elif cash_remained < 0:
            # Для переноса строк код необходимо использовать () вместо бэкслэша \
            # Лучше использовать f-строку для консистентности, а округление сделать заранее
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    # Лишнее переопределение метода
    def get_week_stats(self):
        super().get_week_stats()
