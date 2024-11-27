
import cv2
import json
import base64
import logging
import os
from kafka import KafkaProducer

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def get_frame_from_rtsp(rtsp_url):
    cap = cv2.VideoCapture(rtsp_url)

    if not cap.isOpened():
        logger.error("Не удалось подключиться к RTSP потоку.")
        return None

    while True:
        ret, frame = cap.read()

        if not ret:
            logger.warning("Не удалось получить кадр. Повторная попытка...")
            continue

        resized_frame = cv2.resize(frame, (640, 640))
        _, buffer = cv2.imencode('.jpg', resized_frame)

        frame_as_text = base64.b64encode(buffer).decode('utf-8')

        try:
            producer.send('demo', value={'frame': frame_as_text})
            logger.info("Кадр успешно отправлен в Kafka.")
        except Exception as e:
            logger.error(f"Ошибка при отправке кадра в Kafka: {e}")

        yield resized_frame

    cap.release()
    logger.info("RTSP поток закрыт.")


if __name__ == "__main__":
    try:
        producer = KafkaProducer(
            bootstrap_servers=['kafka:9092'],
            api_version=(0, 11, 5),
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )
        logger.info("KafkaProducer успешно создан.")
    except Exception as e:
        logger.critical(f"Не удалось подключиться к Kafka: {e}")
        exit(1)

    rtsp_url = 'http://158.58.130.148:80/mjpg/video.mjpg'

    for frame in get_frame_from_rtsp(rtsp_url):
        if frame is None:
            logger.info("Завершение работы программы.")
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            logger.info("Программа остановлена пользователем.")
            break
