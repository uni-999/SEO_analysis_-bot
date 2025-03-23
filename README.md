# Telegarm бот для SEO аналитиза

![Logo](https://imgur.com/a/e1lQTbc)

Данный Telegarm бот создан для помощи в нахождении информации о доменах, IP-адресах, файлах, номерах телефонов.

## Описание
Сам Telegram бот является запрос ответной системой для решения задач о поисках информации по открытым источникам.
Основной метод поиска информации реализован на запросах по API-ключам к сайтам. Для реализации были задействованы библиотеки whois.py и requests.py

Разберём что конкретно делает каждая библиотека:
whois - осущетвляет поиск домена или IP-адрема по открытым базам whois сервисов. Результат, полученый входе запроса к базам, обрабатывается путём поиска определённых ключей для получаемого словаря.
requests - осуществляет оправку запросв к базам. В данном проекте инструменты библиотеки помогают в отправке запросов к базам для получение информации о номере телефона или проверки файла.

Сам проект использует и другие инструменты. В обновлении 1.2 добавилась возсожность поиска открытых портов. Сам поиск осуществлен при помощи библиотеки scapy
Scapy — универсальный, поистине мощный инструмент для работы с сетью и проведения исследований в области информационной безопасности. Пока что он применяется для поиска открытых и потенциально уязвимых портов для IP-адресов.
## Установка
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/username/repository.git
