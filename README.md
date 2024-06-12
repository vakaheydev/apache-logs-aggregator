# Агрегатор логов Apache
Агрегатор логов Apache — это приложение, предназначенное для агрегации данных из access логов веб-сервера Apache и сохранения их в базу данных. Приложение поддерживает различные команды и фильтры для запросов и манипуляций с логами.

## Установка и запуск

Склонируйте репозиторий:
``` sh
git clone https://github.com/vakaheydev/apache-logs-aggregator
```
Перейдите в каталог проекта:

``` sh
cd apache-logs-aggregator 
```
Установите зависимости:

``` sh
pip install -r requirements.txt 
```
Настройте конфигурационный файл config.yml в папке resources (конфигурация по умолчанию представлена ниже, в разделе конфигурации).

Запустите приложение:

``` sh
python main.py 
```

# Конфигурация
Приложение настраивается с помощью YAML файла. Ниже приведен пример конфигурации:

*resources/config.yml*:
```yaml
app:
  # Автоматическое агрегирование логов
  schedule_update_logs_enabled: True

  # Интервал агрегирования в секундах
  schedule_update_logs_delay: 30

  # Автоматический запуск веб-сервера Apache
  start_apache_server: True

logs:
  # Формат логов
  format: '%h %l %u %t \"%r\" %>s %b'

  # Путь до папки с логами
  path: server/Apache24/logs

  # Название файла с access логами
  access_log: access.log
```
# Инструкция по использованию
Все запросы совершаются по формату:  
``` sh
*вид запроса* [*параметры запроса*]
```

## Виды запроса  
*get*: получить данные  
*parse*: агрегировать данные из файла в базу данных  
*help*: показать инструкцию ещё раз

## Параметры
### get:
без параметров: без фильтрации  
-ip: фильтр по IP-адресу  
-date: фильтр по дате  
-start_date: фильтр по левой границе интервала даты в логах (используется вместе с end_date)  
-end_date: фильтр по правой границе интервала даты в логах (используется вместе с start_date)  

Примеры использования:
``` sh
get -ip 127.0.0.1
get -ip 127.0.0.1 -date 2024-06-10
get -ip 127.0.0.1 -start_date 2024-06-10 -end_date 2024-06-12
```
# Формат данных
Дата в запросе указывается в формате "yyyy-mm-dd". Примеры:

2024-06-10  
2024-12-31

IP-адрес указывается в стандартном формате "ddd.ddd.ddd.ddd". Примеры:

127.0.0.1  
255.255.255.255

# Выход из приложения
Для выхода из приложения используйте:
``` sh
q
```

Приятного использования!
