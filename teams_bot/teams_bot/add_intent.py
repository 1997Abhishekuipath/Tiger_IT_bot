import pandas as pd
from bot.models.model_bot import Bot
from bot.models.model_intents import Intent
from botData.models.model_entities import Entity
import json
import xlsxwriter


def file_to_db_intent():
    data = pd.ExcelFile('Res_bot_intents.xlsx')
    res = data.parse(data.sheet_names[0])
    webhook_nan = res['webhook'][11]
    for i in range(0, len(res) - 1):
        name = res['name'][i]
        response = res['response'][i]
        webhook = res['webhook'][i]
        bot = Bot.objects.get(id=1)
        webhook = json.loads(webhook) if type(webhook) != type(webhook_nan) else None
        response = json.loads(response) if type(response) != type(webhook_nan) else None
        intent = Intent(name=name, response=response, webhook=webhook, bot_id=bot)
        intent.save()


def file_to_db_entity():
    data = pd.ExcelFile('IT_bot_entities.xlsx')
    res = data.parse(data.sheet_names[0])
    # webhook_nan = res['webhook'][11]
    for i in range(0, len(res)):
        name = res['name'][i]
        response = res['value'][i]
        webhook = res['synonyms'][i]
        intent = Entity(entity_key=name, entity_value=response, entity_synonyms=json.loads(webhook))
        ene = Entity.objects.all()
        for i in ene:
            bot = Bot.objects.filter(id=4)
            i.bot_id.set(bot)
            i.save()
        intent.save()    
        #bot = Bot.objects.filter(id=4)
        
        # intent = Entity(entity_key=name, entity_value=response, entity_synonyms=json.loads(webhook))
        # intent.bot_id.set(bot) # if not working then    delete        this & uncomment        ene  # lines
        
file_to_db_entity()

def db_to_file():
    workbook = xlsxwriter.Workbook('bot_intents.xlsx', options={'remove_timezone': True})
    intents = Intent.objects.filter(bot_id=1)
    worksheet = workbook.add_worksheet()
    for i, intent in enumerate(intents):
        worksheet.write(0, 0, "name")
        worksheet.write(0, 1, "response")
        worksheet.write(0, 2, "webhook")
        worksheet.write(i + 1, 0, intent.name)
        worksheet.write(i + 1, 1, json.dumps(intent.response))
        worksheet.write(i + 1, 2, json.dumps(intent.webhook))
    workbook.close()

# db_to_file()
    # // ene = Entity.objects.all()
    # // for i in ene:
    #     // bot = Bot.objects.filter(id=3)
    # // i.bot_id.set(bot)
    # // i.save()




# def db_to_file_ENTITY():
#     workbook = xlsxwriter.Workbook('IT_bot_intents.xlsx', options={'remove_timezone': True})
#     intents = Intent.objects.filter(bot_id=1)
#     worksheet = workbook.add_worksheet()
#     for i, intent in enumerate(intents):
#         worksheet.write(0, 0, "name")
#         worksheet.write(0, 1, "response")
#         worksheet.write(0, 2, "webhook")
#         worksheet.write(i + 1, 0, intent.name)
#         worksheet.write(i + 1, 1, json.dumps(intent.response))
#         worksheet.write(i + 1, 2, json.dumps(intent.webhook))
#     workbook.close()


# def webhook_change():
#
#
#     web_obj = Intent.objects.filter(bot_id=3, response__isnull=True)
#     web_url = '{"webhook_url": "http://220.227.107.72:8020/webhook/service"}'
#
#     web_url = json.loads(web_url)
#     for i in web_obj:
#         i.webhook = web_url
#         i.save()
# # def file_to_db_entity():
# 	data = pd.ExcelFile('/home/preet/IT_bot_entities.xlsx')
# 	res = data.parse(data.sheet_names[0])
# 	#   webhook_nan = res['webhook'][11]
# 	for i in range(0,133):
#      name = res['name'][i]
#
#      response = res['value'][i]
#      webhook = res['synonyms'][i]
#      intent = Entity(entity_key = name ,entity_value = response, entity_synonyms=json.loads(webhook))
#      bot = Bot.objects.filter(id=1)
#      intent.bot_id.set(bot)

# file_to_db_intent()


# //ene = Entity.objects.all()
# //for i in ene:
#  	//	bot = Bot.objects.filter(id=4)
#  	//	i.bot_id.set(bot)
#  	//	i.save()

