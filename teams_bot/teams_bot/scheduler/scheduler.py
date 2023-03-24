from teams.models import ConversationParameters
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import json
import time


def delete_params():
    date_param = datetime.datetime.now() - datetime.timedelta(minutes=5)
    ConversationParameters.objects.filter(time__lt=date_param).delete()
    # print(ConversationParameters.objects.filter(time__lt=date_param))
    print("Conversation parameters deleted")


# schedule.every(5).minutes.do(delete_params)

# while True:
#  schedule.run_pending()
#  time.sleep(1)


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(delete_params, 'interval', seconds=60)
    scheduler.start()

# run this command in python shell to run scheduler -
# exec(compile(open("/home/preet/teams_bot/scheduler/scheduler.py", "rb").read(),"/home/preet/teams_bot/scheduler/scheduler.py" , 'exec'))