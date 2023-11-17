#!/usr/bin/env python

"""
Functions are written in here

"""

import time
import cv2
import numpy as np
import os
import utils as ut

# Variable
minDiff = 2000
minSquareArea = 2000
vertex = 4

# Load the image from database
ut.readRefImages()


def run(img):

    try:

        print("Running the model")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        edges = ut.auto_canny(blurred)

        contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        #cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
        #cv2.imshow('Contours', img)

        #img = edges

        # Send the Image for checking


        try:
            dymmy, type = ut.checkImage(img, contours, vertex, minSquareArea, minDiff)
        except:
            type = "Checking"
            print(type)

    except:
        print("Error in the runnable model")

    return img, type

if __name__ == '__main__':
    running = True
    cap = cv2.VideoCapture(0)

    while running:
        ret, frame = cap.read()
        frame = run(frame)
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    running = False
    cap.release()
    cv2.destroyAllWindows()
