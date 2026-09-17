University: [ITMO University](https://itmo.ru/ru/)  
Faculty: [FICT](https://fict.itmo.ru)  
Course: [Введение в веб технологии](https://itmo-ict-faculty.github.io/introduction-in-web-tech/)  
Year: 2026/2027  
Group: U4225  
Author: Kupriyanova Arina Vladimirovna  
Lab: Lab1  
Date of create: 17.09.2026  
Date of finished:  

# Лабораторная работа №1

## Основы работы с Docker

## Цель работы

Изучить основы контейнеризации с использованием Docker: научиться работать с образами и контейнерами, использовать Docker volumes, запускать веб-серверы, создавать собственные Dockerfile и собирать Docker-образы.

## Ход работы

### 1. Проверка установки Docker

Была проверена установленная версия Docker:

```bash
docker --version
```

Результат:

```text
Docker version 29.2.1, build a5c7197
```

Также была проверена работа WSL 2, который используется Docker Desktop в Windows.

Для проверки корректности работы Docker был запущен тестовый контейнер:

```bash
docker run hello-world
```

Результат:

```text
Hello from Docker!
This message shows that your installation appears to be working correctly.
```

### 2. Изучение базовых команд Docker

Для просмотра доступных Docker-образов была выполнена команда:

```bash
docker images
```

Для просмотра запущенных контейнеров:

```bash
docker ps
```

Для просмотра всех контейнеров, включая завершённые:

```bash
docker ps -a
```

Эти команды позволяют контролировать состояние образов и контейнеров в Docker.

### 3. Работа с готовым образом Ubuntu

Для загрузки последней версии Ubuntu была выполнена команда:

```bash
docker pull ubuntu:latest
```

После загрузки был запущен интерактивный контейнер:

```bash
docker run -it --name arina-ubuntu-lab1 ubuntu:latest bash
```

Внутри контейнера были обновлены списки пакетов:

```bash
apt update
```

Затем был установлен пакет `curl`:

```bash
apt install -y curl
```

Для проверки установки была выполнена команда:

```bash
curl --version
```

Результат подтвердил, что `curl` успешно установлен и доступен внутри контейнера.

После завершения работы был выполнен выход из контейнера:

```bash
exit
```

### 4. Запуск веб-сервера nginx

Для запуска nginx был создан контейнер с пробросом порта `8080` на порт `80` контейнера:

```bash
docker run -d -p 8080:80 --name arina-web-server nginx:alpine
```

Работа контейнера была проверена командой:

```bash
docker ps
```

После этого в браузере был открыт адрес:

```text
http://localhost:8080
```

В браузере отобразилась стандартная страница:

```text
Welcome to nginx!
```

Для просмотра логов контейнера была выполнена команда:

```bash
docker logs arina-web-server
```

Для подключения внутрь контейнера была выполнена команда:

```bash
docker exec -it arina-web-server sh
```

После проверки был выполнен выход из контейнера:

```bash
exit
```

### 5. Управление контейнером nginx

Контейнер был остановлен командой:

```bash
docker stop arina-web-server
```

После остановки его состояние было проверено:

```bash
docker ps -a --filter "name=arina-web-server"
```

Затем контейнер был снова запущен:

```bash
docker start arina-web-server
```

После повторной проверки контейнер был остановлен и удалён:

```bash
docker stop arina-web-server
docker rm arina-web-server
```

Таким образом была изучена работа основных команд управления контейнерами: запуск, остановка, повторный запуск и удаление.

### 6. Работа с Docker volumes

Для изучения постоянного хранения данных был создан Docker volume:

```bash
docker volume create arina-volume-lab1
```

После этого был запущен контейнер Ubuntu с подключённым томом:

```bash
docker run -it --name arina-volume-test -d -v arina-volume-lab1:/data ubuntu:latest bash
```

Для подключения к контейнеру была выполнена команда:

```bash
docker exec -it arina-volume-test bash
```

Внутри контейнера был создан файл в подключённом томе:

```bash
echo "Hello from volume" > /data/test.txt
```

Содержимое файла было проверено командой:

```bash
cat /data/test.txt
```

Результат:

```text
Hello from volume
```

После этого контейнер был остановлен и удалён:

```bash
docker stop arina-volume-test
docker rm arina-volume-test
```

Затем был создан новый контейнер с подключением того же тома:

```bash
docker run -it --name arina-volume-test-2 -d -v arina-volume-lab1:/data ubuntu:latest bash
```

После подключения к новому контейнеру:

```bash
docker exec -it arina-volume-test-2 bash
```

было повторно проверено содержимое файла:

```bash
cat /data/test.txt
```

Результат:

```text
Hello from volume
```

Это подтверждает, что данные хранятся в Docker volume и сохраняются даже после удаления контейнера.

## Задание со звёздочкой

### 7. Создание Flask-приложения

В папке `lab1` был создан файл `app.py` со следующим содержимым:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello from Docker!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

Также был создан файл `requirements.txt`:

```text
Flask==2.0.1
Werkzeug==2.0.3
Jinja2==3.0.3
```

Дополнительные версии `Werkzeug` и `Jinja2` были зафиксированы для обеспечения совместимости с Flask 2.0.1.

### 8. Создание Dockerfile

Для контейнеризации приложения был создан файл `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y curl vim && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

RUN useradd -m -u 1000 appuser

USER appuser

EXPOSE 5000

ENV FLASK_ENV=production

CMD ["python", "app.py"]
```

Dockerfile выполняет следующие действия:

- использует базовый образ `python:3.9-slim`;
- устанавливает рабочую директорию `/app`;
- устанавливает `curl` и `vim`;
- копирует и устанавливает зависимости из `requirements.txt`;
- копирует Flask-приложение;
- создаёт пользователя `appuser` с UID `1000`;
- переключает выполнение контейнера на пользователя `appuser`;
- открывает порт `5000`;
- задаёт переменную окружения `FLASK_ENV=production`;
- запускает приложение командой `python app.py`.

### 9. Сборка Docker-образа

Для сборки собственного Docker-образа была выполнена команда:

```bash
docker build --no-cache -t my-flask-app .
```

В результате был успешно создан образ:

```text
my-flask-app:latest
```

### 10. Запуск Flask-контейнера

Для запуска приложения была выполнена команда:

```bash
docker run -d -p 5000:5000 --name flask-container my-flask-app
```

Работа контейнера была проверена командой:

```bash
docker ps --filter "name=flask-container"
```

После запуска приложение было проверено запросом:

```bash
curl.exe http://localhost:5000
```

Результат:

```text
Hello from Docker!
```

Это подтверждает, что Flask-приложение успешно работает внутри Docker-контейнера.

### 11. Проверка параметров контейнера

Для проверки пользователя внутри контейнера были выполнены команды:

```bash
whoami
id
```

Контейнер работает от пользователя `appuser` с UID `1000`.

Также были проверены рабочая директория и переменная окружения:

```bash
pwd
echo $FLASK_ENV
```

Результаты:

```text
/app
production
```

Были проверены установленные утилиты:

```bash
curl --version
vim --version
```

Для проверки открытого порта была выполнена команда:

```bash
docker inspect flask-container --format "{{json .Config.ExposedPorts}}"
```

Результат:

```text
{"5000/tcp":{}}
```

## Вывод

В ходе лабораторной работы были изучены основные возможности Docker: работа с образами и контейнерами, запуск интерактивных контейнеров, управление контейнерами, запуск веб-сервера nginx и использование Docker volumes.

Дополнительно было создано Flask-приложение, написан Dockerfile, собран собственный Docker-образ и запущен контейнер с приложением. В результате были получены практические навыки контейнеризации веб-приложений с использованием Docker.

