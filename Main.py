import telebot
from Configuration import bot, vitusTotalAPI, apiUrl
from FindOnRequest import fileSecurityReport
from MessengeCheckers import checkerMessengesWithText


@bot.message_handler(commands=['start', 'help'])
def sendWelcome(message):
    bot.reply_to(message, "Привет, я телеграм-бот, готовый помочь в решении OSINT задач!")


@bot.message_handler(content_types='text')
def checkTextMessenge(message):
    bot.reply_to(message, checkerMessengesWithText(message.text))


@bot.message_handler(content_types=['document', 'photo', 'audio', 'video'])
def checkFileMessenge(message):
        bot.reply_to(message, fileSecurityReport(message))

bot.infinity_polling()