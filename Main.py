import telebot
from Configuration import bot, vitusTotalAPI, apiUrl
from MainMenu import  (start,handle_callback,
                       user_states,triggerDomainSearching,
                       triggerIPSearching,triggerPhoneSearching,
                       triggerFilesAnalyze)

@bot.message_handler(commands=['start', 'help'])
def sendWelcome(message):
    start(message)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    handle_callback(call)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.chat.id
    if user_states.get(user_id) == "waiting_for_domain_request":
        user_states[user_id] = None
        triggerDomainSearching(message)
    elif user_states.get(user_id) == "waiting_for_ip_request":
        user_states[user_id] = None
        triggerIPSearching(message)
    elif user_states.get(user_id) == "waiting_for_phone_request":
        user_states[user_id] = None
        triggerPhoneSearching(message)

@bot.message_handler(content_types=['document', 'photo', 'audio', 'video'])
def checkFileMessenge(message):
    user_id = message.chat.id
    if user_states.get(user_id) == "waiting_for_file_analyze":
        user_states[user_id] = None
        triggerFilesAnalyze(message)

bot.infinity_polling()