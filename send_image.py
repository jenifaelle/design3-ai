import json
import cv2
import base64
import requests
from threading import Thread
from flask import Flask, make_response, jsonify
from collections import deque
import datetime
import time


DELTA_T = 1/15


app = Flask(__name__)


frames = deque()


def read_camera():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, 15)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1600)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1200)
    last_time = time.time()
    while True:
        if time.time() - last_time > DELTA_T:
            last_time = time.time()
            if cap.isOpened():
                ret,image = cap.read()
                if ret:
                    frames.append(image)


@app.route('/take-picture', methods=['POST'])
def take_picture():
    image = frames.pop()
    frames.clear()
    cv2.imwrite("last_picture.jpg", image)

    success, encoded = cv2.imencode('.jpg', image)
    timestamp = time.time()
    body = { "image": base64.b64encode(encoded).decode('utf-8'), "timestamp": timestamp }
    return make_response(jsonify(body))


def main():
    Thread(target=read_camera).start()
    app.run(host='0.0.0.0', port="4000")


if __name__ == '__main__':
    main()

