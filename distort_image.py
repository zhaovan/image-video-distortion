import numpy as np
from scipy import misc
from scipy.interpolate import interp2d
from math import pi, atan2, hypot
import matplotlib.pyplot as plt
import multiprocessing as mp

import time


# Angle of polar cone
maxAngle = pi
minAngle = -maxAngle


# radius of internal code and external cone
minRadius = 100.0
maxRadius = 600.0


def distort_image_to_cone(inputImagePath):

    inputImage = plt.imread(inputImagePath)

    inputImage = np.hstack((inputImage, inputImage, inputImage, inputImage))

    # Vertical Flip
    inputImage = np.array(list(reversed(inputImage)))
    # Horizontal Flip
    inputImage = np.array([list(reversed(row)) for row in inputImage])

    h, w, chn = inputImage.shape

    resultWidth = 1600
    resultHeight = 1200
    centerX = resultWidth / 2
    centerY = resultHeight / 2
    print(f"h = {h} w = {w} chn = {chn}")
    channels = [inputImage[:, :, i] for i in range(3)]
    interpolated = [interp2d(range(w), range(h), c) for c in channels]
    resultImage = np.zeros([resultHeight, resultWidth, 3], dtype=np.uint8)

    start = time.time()
    for c in range(resultWidth):
        print(c)
        for r in range(resultHeight):
            dx = c - centerX
            dy = r - centerY
            angle = np.arctan2(dx, dy)  # yes, dx, dy in this case!
            if angle < maxAngle and angle > minAngle:
                origCol = (angle - minAngle) / (maxAngle - minAngle) * w
                radius = np.hypot(dx, dy)
                if radius > minRadius and radius < maxRadius:
                    origRow = (radius - minRadius) / \
                        (maxRadius - minRadius) * h
                    for chn in range(3):
                        resultImage[r, c, chn] = interpolated[chn](
                            origCol, origRow)
    end = time.time()

    print(end - start)

    plt.imshow(resultImage)
    plt.show()


# distort_image_to_cone()
