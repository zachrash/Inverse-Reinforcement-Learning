import numpy as np
import csv
from math import pi
import cv2


""" Format driving log from Udacity Simulator into [[state, action, state]] """
""" with shape [L, 3] where L is the length of the driving log """
def format(data):
    newdata = np.empty([3, data.shape[1]])
    # Action array
    a = [int(round((float(row[3])*180/2*pi))) for row in data]
    # State array
    s = np.empty((data.shape[1], 256, 256, 3), dtype=np.uint8)
    for i,row in enumerate(data):
        img = cv2.imread(row[0], cv2.CV_LOAD_IMAGE_COLOR)
        s[i, ...] = img.transpose(2, 0, 1)
    # State' array
    s_next = np.empty_like(s)
    for i in range(len(s)-1):
        s_next[i] = s[i+1]

    # Prep for Transpose
    a = np.array(a)[np.newaxis]
    s = s[np.newaxis]
    s_next = s_next[np.newaxis]

    # Transpose
    a = a.T
    s = s.T
    s_next = s_next.T

    # Combine and return
    res = np.concatenate(s, a, s_next)

    return res


def gen():
    # Load CSV
    filename = 'data/driving_log.csv'
    raw_data = open(filename, 'rt')
    data = np.loadtxt(raw_data, dtype='str', delimiter=",")
    data = format(data)

    # Write data to csv
    writer = csv.writer(open("data/trajectories.csv", 'w'))
    for row in data:
        writer.writerow(row)

if __name__ == '__main__':
    gen()
