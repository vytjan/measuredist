The python application analyzing the video stream, detecting a person in it and calculating its walked distance.

Tinkamam programos veikimui reikalingos šios Python bibliotekos:
To run the application the following Python libraries are needed:
OpenCV 3.1.0
matplotlib

Ir šie Python moduliai:
And these python modules:
argparse
datetime
imutils
time
numpy
math

Programos prototipo iškvietimas konsolėje:
To run the prototype on terminal:

a) Norint paleisti vaizdo įvestį iš failo, būtina paduoti --video argumentą
ir vaizdo įrašo failą:
  In order to read a video input stream from the file:
python distance.py --video videos/sample4.mp4

b) Norint naudoti kompiuterio vaizdo kameros filmuojamą vaizdą:
  In order to read a video input stream from the webcam of the computer:
python distance.py

Grafikas nubraižomas matplotlib programa, kai baigiamas apdoroti vaizdo srautas.
The plot is drawn with matplotlib, after the video stream analysis is done.
