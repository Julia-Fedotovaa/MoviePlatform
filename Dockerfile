# Используем базовый образ Python
FROM python:3.13-slim

# Указываем автора
LABEL authors="K1R1EIIIKA"

# Устанавливаем рабочую директорию в корень проекта
WORKDIR /MoviePlatform

# Копируем файлы зависимостей и устанавливаем их
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . .

# Открываем порт для приложения
EXPOSE 8000

# Указываем команду запуска
CMD ["python", "MoviePlatform/manage.py", "runserver_plus", "0.0.0.0:8000", "--cert-file", "cert.crt"]
