FROM python:3.12-slim

# Обновление пакетов и установка необходимых библиотек
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    wget \
    unzip \
    gnupg \
    curl \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgtk-3-0 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libnspr4 \
    libxss1 \
    libxtst6 \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# Установка переменных окружения для Chrome
ENV CHROME_BIN=/usr/bin/chromium
ENV PATH=$PATH:/usr/bin/chromium

# Установка зависимостей Python
WORKDIR /app
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY . .

# Команда запуска
CMD ["python", "main.py"]
