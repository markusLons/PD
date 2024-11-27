import json
import base64
import numpy as np
import cv2
from kafka import KafkaConsumer, KafkaProducer
from ultralytics import YOLO

# Загружаем модель YOLO
model = YOLO("yolov8n.pt")  # Можете использовать любую подходящую модель (например, yolov8n.pt или yolov5s.pt)

# Kafka Consumer
consumer = KafkaConsumer(
    'demo',
    bootstrap_servers=['kafka:9092'],
    api_version=(0, 11, 5),
    auto_offset_reset='earliest',
    group_id='demo',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    api_version=(0, 11, 5),
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# Основной цикл обработки изображений
while True:
    for msg in consumer:
        frame_as_text = msg.value['frame']
        img_data = base64.b64decode(frame_as_text)

        # Декодируем изображение из байтов
        np_arr = np.frombuffer(img_data, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # Детекция с помощью YOLO
        results = model(frame)  # Подаем изображение в модель YOLO

        # Получаем координаты bounding box-ов
        bboxes = []
        for bbox in results.xywh[0]:  # Используем первую (и единственную) картинку из batch
            x_center, y_center, width, height, conf, cls = bbox
            bboxes.append({
                'class': int(cls),
                'confidence': float(conf),
                'x_center': float(x_center),
                'y_center': float(y_center),
                'width': float(width),
                'height': float(height)
            })

        # Выводим координаты bounding box
        print("Bounding boxes:", bboxes)

        # Отправляем результат в Kafka
        producer.send('demo', value={'bb': bboxes})