import cv2
import json

def get_frame_from_rtsp(rtsp_url):
    cap = cv2.VideoCapture(rtsp_url)

    if not cap.isOpened():
        print("Не удалось подключиться к RTSP потоку.")
        return None

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Не удалось получить кадр. Повторная попытка...")
            continue

        resized_frame = cv2.resize(frame, (640, 640))

        yield resized_frame

    cap.release()


if __name__ == "__main__":
    rtsp_url = 'http://158.58.130.148:80/mjpg/video.mjpg'

    for frame in get_frame_from_rtsp(rtsp_url):
        cv2.imshow('RTSP Stream', frame)
        if frame is None:
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
