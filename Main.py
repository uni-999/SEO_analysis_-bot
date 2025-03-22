import telebot
from Configuration import bot, vitusTotalAPI, apiUrl
import requests
import json
import re
import hashlib
import time
from MessengeCheckers import checkerMessengesWithText


@bot.message_handler(commands=['start', 'help'])
def sendWelcome(message):
    bot.reply_to(message, "Привет, я телеграм-бот, готовый помочь в решении OSINT задач!")


@bot.message_handler(content_types='text')
def checkTextMessenge(message):
    bot.reply_to(message, checkerMessengesWithText(message.text))


@bot.message_handler(content_types=['document', 'photo', 'audio', 'video'])
def checkFileMessenge(message):
    file_info = bot.get_file(message.json.get('document', {}).get('file_id'))
    downloadedFile = bot.download_file(file_info.file_path)
    src = 'files/download/' + message.json.get('document', {}).get('file_name')
    with open(src, 'wb') as new_file:
        new_file.write(downloadedFile)
        new_file.close()
    with open(src, "rb") as new_file:
        headers = {
            'x-apikey': vitusTotalAPI
        }
        files = {'file': (src, new_file)}
        response = requests.post(apiUrl, headers=headers, files=files)
        if response.status_code == 200:
            print("Файл успешно загружен:")
            linkOfAnalysis = response.json().get('data', {}).get('links').get('self')
        else:
            print(f"Ошибка при загрузке файла: {response.status_code}")
            print(response.text)
        while True:
            response = requests.get(linkOfAnalysis, headers=headers)
            if response.status_code == 200:
                analysisData = response.json()
                status = analysisData['data']['attributes']['status']
                print(f"Статус анализа: {status}")

                if status == 'completed':
                    print("Анализ завершен!")
                    break
                elif status in ['queued', 'in-progress']:
                    print("Анализ еще не завершен. Ожидание...")
                    time.sleep(20)  # Подождать 20 секунд перед следующим запросом
                else:
                    print(f"Неизвестный статус анализа: {status}")
                    break
            else:
                print(f"Ошибка при проверке статуса анализа: {response.status_code}")
                print(response.text)
                break
        if status == 'completed':
            results = analysisData['data']['attributes']['results']
            stats = analysisData['data']['attributes']['stats']

        finalMessage = "📊 Результаты анализа файла:\n"
        finalMessage += f"✅ Безопасных: {stats.get('harmless', 0)}\n"
        finalMessage += f"⚠️ Подозрительных: {stats.get('suspicious', 0)}\n"
        finalMessage += f"❌ Вредоносных: {stats.get('malicious', 0)}\n"
        finalMessage += f"❓ Неопределенных: {stats.get('undetected', 0)}\n\n"

        # Детали от каждого антивируса
        finalMessage += "🔍 Детали анализа:\n"
        for engine, result in results.items():
            category = result.get('category', 'unknown')
            detection = result.get('result', 'нет данных')
            engine_name = result.get('engine_name', engine)

            finalMessage += f"- {engine_name}: "
            if category == 'malicious':
                finalMessage += f"⚠️ ВРЕДОНОСНЫЙ ({detection})\n"
            elif category == 'suspicious':
                finalMessage += f"⚠️ ПОДОЗРИТЕЛЬНЫЙ ({detection})\n"
            elif category == 'harmless':
                finalMessage += f"✅ БЕЗОПАСНЫЙ\n"
            else:
                finalMessage += f"❓ НЕОПРЕДЕЛЕННЫЙ\n"

        # Вывод сообщения
        bot.reply_to(message, finalMessage)

        # files = dict(file=(src, new_file))
        # response = requests.post(apiUrl, files=files, params=vitusTotalAPI)
        # if response.status_code == 200:
        #     result = response.json()
        #     print(json.dumps(result, sort_keys=False, indent=4))
        # print(response.status_code)
    # try:
    #     print(client.get_object("/files/" + get_file_hash(src)))
    # except:
    #     with open(src, "rb") as f:
    #         analysis = await client.scan_file(f, wait_for_completion=True)
    #         f.close()
    #     print(analysis)


def get_file_hash(file_path):
    hashType = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            hashType.update(chunk)
    return hashType.hexdigest()


bot.infinity_polling()