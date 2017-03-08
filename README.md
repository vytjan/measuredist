The python application analyzing the video stream, detecting a person in it and calculating its walked distance.

To run the application the following Python libraries are needed:
OpenCV 3.1.0
matplotlib

And these python modules:
argparse
datetime
imutils
time
numpy
math


To run the prototype on terminal:

a) In order to read a video input stream from the file:
python distance.py --video videos/sample4.mp4

b) In order to read a video input stream from the webcam of the computer:
python distance.py

The plot is drawn with matplotlib, after the video stream analysis is done.
