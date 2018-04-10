import numpy as np
import csv
from math import pi
import cv2
from keras.preprocessing.image import img_to_array, load_img, flip_axis


""" Format driving log from Udacity Simulator into [[state, action, state]] """
""" with shape [L, 3] where L is the length of the driving log """
def format(data):
    newdata = np.empty([3, data.shape[1]])
    # Action array
    a = [int(round((float(row[3])*180/2*pi))) for row in data]
    a = np.array(a, dtype=np.float32)
    # State array
    s = np.empty([data.shape[0], 160, 320, 3], dtype=np.float32)
    for i,row in enumerate(data):
        image = load_img(row[0])
        image = img_to_array(image)
        image = (image / 255. - .5).astype(np.float32)
        s[i] = image
    # State' array
    s_next = np.empty_like(s)
    for j in range(len(s)-1):
        s_next[j] = s[j+1]

    return a, s, s_next


def generate_trajectories():
    # Load CSV
    filename = 'data/driving_log.csv'
    raw_data = open(filename, 'rt')
    data = np.loadtxt(raw_data, dtype='str', delimiter=",")
    a, s, s_next = format(data)

    # Write data to csv -> [[state, action, state']] with shape [N, 3]
    writer = csv.writer(open("data/trajectories.csv", 'w'))
    for i in range(len(a)-1):
        writer.writerow((s[i], a[i], s_next[i]))
