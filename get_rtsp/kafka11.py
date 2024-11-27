import json
import base64
import cv2
import numpy as np
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'demo',
    bootstrap_servers=['localhost:9092'],
    api_version=(0, 11, 5),
    auto_offset_reset='earliest',
    group_id='demo',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for msg in consumer:
    frame_as_text = msg.value['frame']
    img_data = base64.b64decode(frame_as_text)

    np_arr = np.frombuffer(img_data, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    cv2.imshow('Received Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
