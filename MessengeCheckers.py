import re
from fake_useragent import UserAgent
from FindOnRequest import findIp, findDomain, findPhoneNumber

def generateUseragent() -> str:
    fua = UserAgent()
    return str(fua.random)

def checkerForMessageWithDomain(message):
    domainPattern = r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    urlPattern = r'^(https?|ftp)://[^\s/$.?#].[^\s]*$'
    if re.match(domainPattern, message) or re.match(urlPattern, message):
        return (findDomain(message))
    else:
        return None

def checkerForMessageWithIP(message):
    ipPattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if re.match(ipPattern, message):
        return(findIp(message, generateUseragent()))
    else:
        return None

def checkerForMessageWithPhone(message):
    phonePattern = r'^\+?[1-9]\d{1,14}$'
    if re.match(phonePattern, message):
        return (findPhoneNumber(message, generateUseragent()))
    else:
        return None