# coding=utf-8
import telebot
import logging
import requests
import json
import ast

FORMAT = '[%(asctime)s] [%(levelname)s] [%(message)s]'
logging.basicConfig(filename="logs.txt", format=FORMAT, level=logging.INFO)
logging.info("Server Basladi.")

bildirim = False
bot = telebot.TeleBot("<<TELEGRAM-BOT-TOKEN>>")
data = {}

with open("data", "r") as gelen:
    data = ast.literal_eval(gelen.read())
logging.info("Mesajlar Oluşturuldu")


def bildirimal(message):
    global bildirim
    with open("bildirimler.txt","a") as bilfile:
        bilfile.write("[{}] [{}] [{}] \n".format(message.from_user.username,message.from_user.first_name+message.from_user.last_name,message.text))
    bot.send_message(message.chat.id,"{}({}) Bildirimini aldık belki şuan okuyoruz. En yakın sürede dönüş/düzenleme yapılacak.".format(message.from_user.first_name,message.from_user.username))
    bildirim = False


def cevapver(message):
    for i in data.keys():
        if message.text.lower().find(i) > -1:
            bot.send_message(message.chat.id,data.get(i))
            logging.info("{} ile ilgili Cevap Gönderildi".format(i))
            return True
    return False


def ceydayasor(message):
    try:
        arg = {'username': '<<CEYD-A-USERNAME>>', 'token': '<<CEYD-A-TOKEN>>','code': message.text.lower() ,'type':'text'}
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


@bot.message_handler(commands=['start'])
def send_welcome(message):
    logging.info("-{}- mesajı alındı.".format(message.text))
    bot.send_message(message.chat.id,"Merhaba {} nasıl yadımcı olabilirim?".format(message.from_user.first_name))
    logging.info("Hoşgeldin Mesajı Gönderildi.")

@bot.message_handler(commands=['bildirim'])
def send_welcome(message):
    global bildirim
    logging.info("Bildirim alınacak.")
    bot.send_message(message.chat.id,"Merhaba {}. İstek dilek ve Şikayetlerini Buraya Yazabilirsin".format(message.from_user.first_name))
    bildirim = True

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    global bildirim
    logging.info("{}- mesajı alındı.".format(message.text))
    if bildirim == True:
        bildirimal(message)
    else:
        if cevapver(message) == False:
            logging.info("Cevap Bulunamadı Ceyd-a ya soruluyor..")
            ceydayasor(message)

bot.polling()
