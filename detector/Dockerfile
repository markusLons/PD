# Используем готовый образ ультралитикс для ARM64
FROM ultralytics/ultralytics:latest-arm64

# Устанавливаем необходимые библиотеки для Kafka и OpenCV
RUN pip install --no-cache-dir \
    kafka-python \
    opencv-python-headless \
    numpy \
    pillow \
    requests

# Создаем директорию для приложения
WORKDIR /app

# Копируем ваш Python скрипт в контейнер
COPY main.py /app/main.py

# Указываем команду для запуска скрипта
CMD ["python", "main.py"]