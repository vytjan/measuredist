# -*- coding: utf-8 -*-
# import the necessary packages
# A4 - 210 x 297 mm - size of greenboard measure unit (width).
# Therefore, the width of the greenboard is ~ 14*21 = 294 ~= 300 cm
import argparse
import datetime
import imutils
import time
import cv2
import numpy as np
import math
import matplotlib.pyplot as plt

# construct the argument parser and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-v", "--video", help="path to the video file")
# args = vars(ap.parse_args())

import sys
 
total = len(sys.argv)
del sys.argv[0]
del sys.argv[0]
cmdargs = str(sys.argv)

print(cmdargs);
print ("The total numbers of args passed to the script: %d " % total)
print ("Args list: %s " % cmdargs)
 

print ("First argument: %s" % str(sys.argv[0]))
# print args;

# initialize the width of the greenboard
greenboardWidth = 300
# initialize the first frame in the video stream
firstFrame = None
t0 = time.clock()
start = 0
end = 0

# initialize distance algorithm vars
distance = 0
timeLap = []
xcoordinates = []
x1 = 0
x2 = 0
x3 = 0
cmperpix = 0
leftx = 0
rightx = 0

# read from webcam if no video argument
if not cmdargs:
  camera = cv2.VideoCapture(1)
  time.sleep(0.25)

# or read the video file
else:
  frameCounter = 1
  for number in sys.argv:

    camera = cv2.VideoCapture(number)


    # data for x axis of the plot
    
    while True:
      # grab the current frame.
      (grabbed, frame) = camera.read()
      
      # if the frame could not be grabbed, then we have reached the end
      # of the video
      if not grabbed:
        break
     
      # resize the frame, convert it to grayscale, and blur it
      frame = imutils.resize(frame, width=500)
      gray = cv2.medianBlur(frame,5)
      gray = cv2.GaussianBlur(gray, (5, 5), 0)
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

      gray = cv2.GaussianBlur(gray, (5, 5), 0)
      # splitting the channels of hsv
      h,s,v = cv2.split(gray)
     
      # if the first frame is None, initialize it
      if firstFrame is None:
        firstFrame = v
        grayInit = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        grayInit = cv2.GaussianBlur(grayInit, (3, 3), 0)

        # detect edges in the image
        edged = cv2.Canny(grayInit, 10, 250)

        # construct and apply a closing kernel to 'close' gaps between 'white'
        # pixels
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)

        (ima, cn, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # loop over the contours
        if cn:
          areas = [cv2.contourArea(c1) for c1 in cn]
          max_index = np.argmax(areas)
          c1=cn[max_index]
          # approximate the contour
          peri = cv2.arcLength(c1, True)
          approx = cv2.approxPolyDP(c1, 0.05 * peri, True)

          M1 = cv2.moments(c1)
          if( M1['m00'] != 0):
            centrx = int(M1['m10']/M1['m00'])
            centry = int(M1['m01']/M1['m00'])
            (leftx, lefty) = tuple(c1[c1[:,:,0].argmin()][0])
            (rightx, righty) = tuple(c1[c1[:,:,0].argmax()][0])
            widthinpix = rightx - leftx;
            cmperpix = greenboardWidth / float(widthinpix);
            # print leftx, rightx, cmperpix;

          # if the approximated contour has four points, then assume that the
          # contour is a rectangle

        continue
      if len(approx) == 4:

        cv2.drawContours(frame, [approx], -1, (0, 255, 0), 4)
        
    # compute the absolute difference between the current frame and the initial one
      frameDelta = cv2.absdiff(firstFrame, v)

      thresh = cv2.threshold(frameDelta, 60, 255, 0)[1]
      # thresh = cv2.erode(thresh, (5,5), iterations=20)
      thresh = cv2.dilate(thresh, (40,40), iterations=20)
      thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, (5,5))
      thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, (5,5))

      (imb, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)

      # centroid coord var:
      # loop over the contours
      if cnts:
        areas = [cv2.contourArea(c) for c in cnts]
        max_index = np.argmax(areas)
        cnt=cnts[max_index]

        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)

        # finding a centroid of a contour area:
        M = cv2.moments(c)
        if( M['m00'] != 0):
          cx = int(M['m10']/M['m00'])
          cy = int(M['m01']/M['m00'])

          # calculate distance:
          if (cx >= leftx and cx <= rightx):
            if not x1:
              if(cx < ((rightx - leftx)/2)):
                distance += (cx - leftx) * cmperpix;
              else:
                distance += (rightx - cx) * cmperpix;
              x1 = cx;
            else:
              # print cx, x1;
              if(cx > x1):
                distance += (cx - x1) * cmperpix;
              else:
                distance += (x1 - cx) * cmperpix;
              x1 = cx;

          timing = 0.04 * frameCounter;
          xcoordinates.append(cx)
          timeLap.append(timing)
     
      # show the frame and record if the user presses a key
      cv2.imshow("Security Feed", frame)
      cv2.imshow("Thresh", thresh)
      cv2.waitKey(25)

      frameCounter += 1;
      # if the `q` key is pressed, break from the lop
      # if key == ord("q"):
      #   break
    firstFrame = None
    x1 = 0
# cleanup the camera and close any open windows
print('Nueitas atstumas yra: ');
print(distance);
camera.release()
cv2.destroyAllWindows()

plt.rc('font', family='DejaVu Sans')

# Plotting
plt.plot(timeLap, xcoordinates)

plt.xlabel(u'Laikas, (s)')
plt.ylabel(u'X koordinatės')
plt.title(u'Žmogaus kontūro centro koordinatės')
plt.grid(True)
plt.savefig("plot.png")
plt.show()