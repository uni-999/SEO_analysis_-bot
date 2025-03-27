import requests
import telebot
import whois as pywhois
from Configuration import bot, vitusTotalAPI, apiUrl
import time
from InputDict import dictForSearch
from scapy.all import *

def formatDates(dateList):
    if not isinstance (dateList, list):
        dateList = [dateList] if dateList is not None else ['N/A']
    elif not dateList:
        dateList = ['N/A']
    return [str(date) for date in dateList]

def findDomain(message):
    w = pywhois.whois(message)
    finalMessange = ""
    for key, value in dictForSearch.items():
        if isinstance(value, list):
            finalMessange += processList(key, value, w)
        else:
            finalMessange += processString(key, value, w)
    return finalMessange

def processList(key, value, w) -> str:
    """Обрабатывает список, возвращает строку для вывода  ヾ(＾∇＾)"""
    for i in value:
        SourceData = w.get(i, 'N/A')
        if SourceData == 'N/A':
            dataInIndex = SourceData
            continue
        if isinstance(SourceData, list):
            dataInIndex = ', '.join(formatDates(SourceData))
            break
        else:
            dataInIndex = SourceData
            break

    return f"{key}: {dataInIndex} \n"

def processString(key, value, w) -> str:
    """Обрабатываем строку и возвращаем строку  ヾ(＾∇＾)"""

    SourceData = w.get(value, 'N/A')
    if isinstance(SourceData, list):
        dataInIndex = ', '.join(formatDates(SourceData))
        return f"{key}: {dataInIndex}\n"
    else:
        dataInIndex = SourceData
        return f"{key}: {dataInIndex}\n"

def findIp(ipAddress, fua):
    result = str()
    try:
        headers = {
            'User-Agent': fua
        }
        data = requests.get(f'https://ipinfo.io/{ipAddress}/json', headers=headers).json()
    except Exception as ex:
        return ex
    message = (
        f"IP-адрес: {data.get('ip', 'N/A')}\n"
        f"Открытые порты: {str(findOpenPortsByIP(ipAddress))}\n"
        f"Хостнейм: {data.get('hostname', 'N/A')}\n"
        f"Город: {data.get('city', 'N/A')}\n"
        f"Регион: {data.get('region', 'N/A')}\n"
        f"Страна: {data.get('country', 'N/A')}\n"
        f"Координаты: {data.get('loc', 'N/A')}\n"
        f"Организация: {data.get('org', 'N/A')}\n"
        f"Почтовый индекс: {data.get('postal', 'N/A')}\n"
        f"Часовой пояс: {data.get('timezone', 'N/A')}\n"
        f"Anycast: {'Да' if data.get('anycast', False) else 'Нет'}"
    )
    return message

def findPhoneNumber(phonenumber, fua):
    try:
        url = f"https://htmlweb.ru/geo/api.php?json&telcod={phonenumber}"
        headers = {
            'User-Agent': fua
        }
        data = requests.get(url, headers=headers).json()
    except Exception as ex:
        return ex
    print(data)
    message = (
        f"Страна: {data.get('country', {}).get('name', 'N/A')}\n"
        f"Регион: {data.get('region', {}).get('name', 'N/A')}\n"
        f"Район: {data.get('region', {}).get('okrug', 'N/A')}\n"
        f"Оператор: {data.get('0', {}).get('oper', 'N/A')}\n"
        f"Часть света: {data.get('country', {}).get('location', 'N/A')}"
    )
    return message

def findOpenPortsByIP(ipAddress):
    openPorts = []
    packets = [IP(dst=ipAddress) / TCP(dport=port, flags="S") for port in range(1, 1025)]
    responses, _ = sr(packets, timeout=2, verbose=0)
    for sent, received in responses:
        if received.haslayer(TCP) and received[TCP].flags == 0x12:  # SYN-ACK
            openPorts.append(sent[TCP].dport)
            sr1(IP(dst=ipAddress) / TCP(dport=sent[TCP].dport, flags="R"), timeout=0.1, verbose=0)
    result = ', '.join(map(str, openPorts))
    return result

def fileSecurityReport(message):
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
        bot.reply_to(message, finalMessage)