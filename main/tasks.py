import logging
from datetime import timedelta
import schedule
import time, datetime
from .models import Subscriber
import os
log_file_path = os.path.join('C:/Dip/v1/website', 'subscriptions.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s %(message)s')

def charge_subscriptions():
    subscribers = Subscriber.objects.all()

    for subscriber in subscribers:
        internet_package = subscriber.package
        tv_package = subscriber.tv_package

        internet_fee = internet_package.price / 30
        tv_fee = tv_package.price / 30

        if subscriber.balance > 0:
            if subscriber.balance >= internet_fee + tv_fee:
                subscriber.balance -= internet_fee + tv_fee
            else:
                subscriber.balance = 0

            subscriber.save()
            log_message = f"Дата списання: {datetime.datetime.now()}, Почта клієнта: {subscriber.email}, " \
                          f"Сумма списання: {internet_fee + tv_fee}, Сумма залишку: {subscriber.balance}"
            logging.info(log_message)
            print(log_message)

schedule.every().day.at('03:00').do(charge_subscriptions)
#schedule.every(10).seconds.do(charge_subscriptions)
while True:
    schedule.run_pending()
    time.sleep(1)



# Запланировать выполнение задачи каждые 10 секунд
#schedule.every(10).seconds.do(charge_subscriptions)


#запуск celery -A website worker --loglevel=info
