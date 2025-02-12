from telegram import Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler
import logging
from generator import checkMessage, answerStart

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

if __name__ == '__main__':
    application = ApplicationBuilder().token('Enter Your Code').build()

    startHandler = CommandHandler('start', answerStart)
    echoHandler = MessageHandler(filters.TEXT & (~filters.COMMAND), checkMessage)
    
    application.add_handler(startHandler)
    application.add_handler(echoHandler)

    application.run_polling()