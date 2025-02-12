from telegram import Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler
from finder import findIp, findDomain, findPhoneNumber
import re
from fake_useragent import UserAgent
from proto import findDomainTester

def generateUseragent() -> str:
    fua = UserAgent()
    return str(fua.random)

async def answerStart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Привет, я телеграм-бот, готовый помочь в решении OSINT задач!")

async def checkMessage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    urlPattern = r'^(https?|ftp)://[^\s/$.?#].[^\s]*$'
    phonePattern = r'^\+?[1-9]\d{1,14}$'
    ipPattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    domainPattern = r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if re.match(phonePattern, message):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=findPhoneNumber(message, generateUseragent()))
    elif re.match(ipPattern, message):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=findIp(message, generateUseragent()))
    elif re.match(domainPattern, message) or re.match(urlPattern, message):
        findDomainTester(message)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=findDomain(update.message.text))
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Неизвестный формат сообщения")