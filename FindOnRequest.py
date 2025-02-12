import requests
import whois
from InputDict import dictForSearch

def formatDates(dateList):
    if not isinstance (dateList, list):
        dateList = [dateList] if dateList is not None else ['N/A']
    elif not dateList:
        dateList = ['N/A']
    return [str(date) for date in dateList]

def findDomain(messange) -> str:
    w = whois.whois(messange)
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

def findIp(ipaddr, fua):
    result = str()
    try:
        headers = {
            'User-Agent': fua
        }
        data = requests.get(f'https://ipinfo.io/{ipaddr}/json', headers=headers).json()
    except Exception as ex:
        return ex
    message = (
        f"IP-адрес: {data.get('ip', 'N/A')}\n"
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