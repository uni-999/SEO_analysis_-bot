import telebot
from telebot import types
from Configuration import bot
from MessengeCheckers import checkerForMessageWithIP,checkerForMessageWithPhone,checkerForMessageWithDomain
from FindOnRequest import fileSecurityReport

user_states = {}

def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    buttonInformation = types.InlineKeyboardButton("📝 О боте", callback_data="about")
    buttonServices = types.InlineKeyboardButton("👾 Услуги", callback_data="services")
    buttonContacts = types.InlineKeyboardButton("📇 Контакты", callback_data="contacts")
    markup.add(buttonContacts, buttonServices, buttonInformation)

    bot.send_message(
        message.chat.id,
        "Добро пожаловать, хакер 😎\nВыберите интересующий вас раздел:",
        reply_markup=markup
    )
def getDataAbout(call, markup):
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="👋 Здравствуйте!\n"
             "🌐 Я - бот, который поможет вам в поиске данных об IP-адресах, доменах, номерах телефонов!\n"
             "👀 Ко всему этому, я имею расширенный функционал: смогу проверить любой файл на наличие любого рода вредоносов, "
             "найти уязвимые порты серверов\n"
             "❗️ Хочу подметить, что я создан исключительно в обучающих целях, и не несу ответственности за ваше использование данной информации.",
        reply_markup=markup)

def getDataContact(call, markup):
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="🌐 Бот создан Шараповым Дмитрием, студентом Казанского федерального университета\n"
             "✉️ Мой телеграм - @uni_999\n"
             "📟 Мой Discord - unitou\n"
             "🛠 Мой GitHub - https://github.com/uni-999\n"
             "❗️ Хочу подметить, что бот создан исключительно в обучающих целях.Я несу ответственности за ваше использование данной ботом информацией.",
        reply_markup=markup)


def handle_callback(call):
    if call.data == "about":
        markup = types.InlineKeyboardMarkup(row_width=1)
        buttonBack = types.InlineKeyboardButton("🔙 Назад", callback_data="back_to_main")
        markup.add(buttonBack)
        getDataAbout(call, markup)

    elif call.data == "contacts":
        markup = types.InlineKeyboardMarkup(row_width=1)
        buttonBack = types.InlineKeyboardButton("🔙 Назад", callback_data="back_to_main")
        markup.add(buttonBack)
        getDataContact(call, markup)

    elif call.data == "services":
        markup = types.InlineKeyboardMarkup(row_width=1)
        buttonDomain = types.InlineKeyboardButton("💻 Поиск по домену", callback_data="domain_searching")
        buttonIp = types.InlineKeyboardButton("🌐 Поиск по IP-адресу", callback_data="ip_searching")
        buttonPhone = types.InlineKeyboardButton("📱 Поиск по номеру телефона",callback_data="phone_searching")
        buttonFileAnalyzis = types.InlineKeyboardButton("📊 Проверка файла на вирусы", callback_data="file_analyze_searching")
        buttonBack = types.InlineKeyboardButton("🔙 Назад", callback_data="back_to_main")

        markup.add(buttonDomain, buttonIp, buttonPhone, buttonFileAnalyzis,buttonBack)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Выберите тип услуги:",
            reply_markup=markup
        )
    elif call.data == "back_to_main":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        start(call.message)
    elif call.data == "domain_searching":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(call.message.chat.id, "Введите домен либо его ссылку:")
        user_states[call.from_user.id] = "waiting_for_domain_request"
    elif call.data == "ip_searching":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(call.message.chat.id, "Введите IP-адрес:")
        user_states[call.from_user.id] = "waiting_for_ip_request"
    elif call.data == "phone_searching":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(call.message.chat.id, "Введите номер телефона:")
        user_states[call.from_user.id] = "waiting_for_phone_request"
    elif call.data == "file_analyze_searching":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(call.message.chat.id, "Отправьте файл для проверки:")
        user_states[call.from_user.id] = "waiting_for_file_analyze"

def triggerDomainSearching(message):
    finalMessage = checkerForMessageWithDomain(message.text.strip())
    if finalMessage != None:
        bot.reply_to(message, finalMessage)
        start(message)
    else:
        bot.reply_to(message, "Произошла ошибка при поиске информации по введёному домену. Проверьте его корректность")
        start(message)

def triggerIPSearching(message):
    finalMessage = checkerForMessageWithIP(message.text.strip())
    if finalMessage != None:
        bot.reply_to(message, finalMessage)
        start(message)
    else:
        bot.reply_to(message, "Произошла ошибка при поиске информации по введёному IP. Проверьте его корректность")
        start(message)

def triggerPhoneSearching(message):
    finalMessage = checkerForMessageWithPhone(message.text.strip())
    if finalMessage != None:
        bot.reply_to(message, finalMessage)
        start(message)
    else:
        bot.reply_to(message, "Произошла ошибка при поиске информации по введёному номеру телефона. Проверьте его корректность")
        start(message)

def triggerFilesAnalyze(message):
    fileSecurityReport(message)
    start(message)