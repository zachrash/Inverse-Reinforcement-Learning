import argparse
import h5py
import base64
from flask import Flask, render_template
from io import BytesIO
from PIL import Image
import eventlet
import eventlet.wsgi
import numpy as np
import socketio
from keras import __version__ as keras_version
from keras.models import load_model
from keras.preprocessing.image import img_to_array, load_img, flip_axis

sio = socketio.Server()
app = Flask(__name__)
target_speed = 22
shape = (100, 100, 3)

def preprocess(image):
    image = load_img(image)
    image = img_to_array(image)
    image = (image / 255. - .5).astype(np.float32)
    return image

@sio.on('telemetry')
def telemetry(sid, data):
    # The current image from the center camera of the car
    img_str = data["image"]
    speed = float(data["speed"])

    # Set the throttle.
    throttle = 1.2 - (speed / target_speed)

    # read and process image
    image_bytes = BytesIO(base64.b64decode(img_str))
    image = preprocess(image_bytes)

    sa = agent.act(image)

    print(sa, throttle)
    send_control(sa, throttle)

@sio.on('connect')
def connect(sid, environ):
    print("connect ", sid)
    send_control(0, 0)

def send_control(steering_angle, throttle):
    sio.emit("steer", data={
    'steering_angle': steering_angle.__str__(),
    'throttle': throttle.__str__()
    }, skip_sid=True)

def drive():
    for e in range(agent.episodes):
        state =
        done = False
        while not done:
            action = agent.act()

if __name__ == '__main__':
    agent = DQN((160, 320, 3), 360)
    #agent.load("/save/model.h5")

    app = socketio.Middleware(sio, app)

    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 4567)), app)
