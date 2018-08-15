# coding=utf-8
import telebot
import logging
import requests
import json
import ast

FORMAT = '[%(asctime)s] [%(levelname)s] [%(message)s]'
logging.basicConfig(filename="logs.txt", format=FORMAT, level=logging.INFO)
logging.info("Server Basladi.")

cevap = False
bot = telebot.TeleBot("<<TELEGRAM-BOT-TOKEN>>")
data = {}

with open("data", "r") as gelen:
    data = ast.literal_eval(gelen.read())
logging.info("Mesajlar Oluşturuldu")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    logging.info("-{}- mesajı alındı.".format(message.text))
    bot.send_message(message.chat.id,"Merhaba {} nasıl yadımcı olabilirim?".format(message.from_user.first_name))
    logging.info("Hoşgeldin Mesajı Gönderildi.")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    global cevap
    logging.info("{}- mesajı alındı.".format(message.text))
    gelen = message.text.lower()

    for i in data.keys():
        if gelen.find(i) > -1:
            bot.send_message(message.chat.id,data.get(i))
            cevap = True
            logging.info("{} ile ilgili Cevap Gönderildi".format(i))

    if cevap == False:
        logging.info("Cevap Bulunamadı Ceyd-a ya soruluyor..")
        try:

            arg = {'username': '<<CEYD-A-USERNAME>>', 'token': '<<CEYD-A-TOKEN>>','code': gelen ,'type':'text'}
            r= requests.post("http://beta.ceyd-a.com/jsonengine.jsp", data=arg).content.decode('utf-8')[1:-3]
            cevap = json.loads(r).get("answer")

            if cevap != '':
                bot.send_message(message.chat.id,cevap)
                logging.info("Ceyd-a cevap verdi : {}".format(cevap))
            else:
                bot.send_message(message.chat.id,"Ceyd-A API Beta sürümünde çalıştığı için bazı komutlarda eksilik var. Play Store dan tam sürümü indirip bu komutu tekrar deneyebilirsin.")
                logging.info("Ceyd-a boş yapti. : {}".format(r))

        except Exception as e:
            bot.send_message(message.chat.id,"Bir hata oluştu ve bildirildi. En yakın zamanda düzeltilecek.")
            logging.error(e)

    cevap = False

bot.polling()
