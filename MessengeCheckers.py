import re
from fake_useragent import UserAgent
from FindOnRequest import findIp, findDomain, findPhoneNumber

def generateUseragent() -> str:
    fua = UserAgent()
    return str(fua.random)

def checkerMessengesWithText(message):
    urlPattern = r'^(https?|ftp)://[^\s/$.?#].[^\s]*$'
    phonePattern = r'^\+?[1-9]\d{1,14}$'
    ipPattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    domainPattern = r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if re.match(phonePattern, message):
        return (findPhoneNumber(message, generateUseragent()))
    elif re.match(ipPattern, message):
        return(findIp(message, generateUseragent()))
    elif re.match(domainPattern, message) or re.match(urlPattern, message):
        return (findDomain(message))
    else:
        return("Неизвестный формат сообщения")

# def checkerMessengesWithFiles(messenge):
#