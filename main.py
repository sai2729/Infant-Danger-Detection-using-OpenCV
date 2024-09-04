from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2    #computer vision library
from scipy.spatial import distance as dist
import pyttsx3
import playsound
from tkinter import *



engine = pyttsx3.init()



def distract():
	playsound.playsound('baby.wav', True)


def start_watching():
	dangerCount = voiceCount = zoneValue = 0
	voiceAssisName = ""
	# -------------------------cv2----------------------------------
	engine = pyttsx3.init()

	# construct the argument parser and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-v", "--video", type=str, help="path to input video file")
	ap.add_argument("-t", "--tracker", type=str, default="kcf", help="OpenCV object tracker type")
	args = vars(ap.parse_args())

	# initialize a dictionary that maps strings to their corresponding
	# OpenCV object tracker implementations

	OPENCV_OBJECT_TRACKERS = {
		"csrt": cv2.TrackerCSRT_create,
		"kcf": cv2.TrackerKCF_create,
		"boosting": cv2.TrackerBoosting_create,
		"mil": cv2.TrackerMIL_create,
		"tld": cv2.TrackerTLD_create,
		"medianflow": cv2.TrackerMedianFlow_create,
		"mosse": cv2.TrackerMOSSE_create
	}

	trackers = cv2.MultiTracker_create()

	track_count = 0

	# if a video path was not supplied, grab the reference to the web cam
	if not args.get("video", False):
		print("[INFO] starting video stream...")
		vs = VideoStream(src=1).start()
		time.sleep(1.0)

	# otherwise, grab a reference to the video file
	else:
		vs = cv2.VideoCapture(args["video"])

	# loop over frames from the video stream
	while True:
		# grab the current frame, then handle if we are using a
		# VideoStream or VideoCapture object
		frame = vs.read()
		frame = frame[1] if args.get("video", False) else frame

		# check to see if we have reached the end of the stream
		if frame is None:
			break

		# resize the frame (so we can process it faster)
		frame = imutils.resize(frame, width=1000)

		# grab the updated bounding box coordinates (if any) for each
		# object that is being tracked
		(success, boxes) = trackers.update(frame)

		if len(boxes) == 0:
			frame = cv2.putText(frame, "select the " + childName.get(), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 2,
								[0, 0, 255], 2)
		if len(boxes) == 1:
			child = boxes[0]
			frame = cv2.putText(frame, "select the " + dangerName.get() + " place", (100, 100),
								cv2.FONT_HERSHEY_SIMPLEX, 2,
								[0, 0, 255], 2)

		# loop over the bounding boxes and draw then on the frame
		for box in boxes:
			(x, y, w, h) = [int(v) for v in box]
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

		print(len(boxes))
		if len(boxes) >= 2:
			stack_x = []
			stack_y = []
			stack_x_print = []
			stack_y_print = []
			global D
			count = 0

			for boxi in boxes:
				(x, y, w, h) = [int(v) for v in boxi]
				x1 = x
				y1 = y
				x2 = x + w
				y2 = y + h
				mid_x = int((x1 + x2) / 2)
				mid_y = int((y1 + y2) / 2)
				stack_x.append(mid_x)
				stack_y.append(mid_y)
				stack_x_print.append(mid_x)
				stack_y_print.append(mid_y)
				count = count + 1
			D = int(dist.euclidean((stack_x.pop(), stack_y.pop()), (stack_x.pop(), stack_y.pop())))
			frame = cv2.line(frame, (stack_x_print.pop(), stack_y_print.pop()),
							 (stack_x_print.pop(), stack_y_print.pop()),
							 [0, 0, 255], 2)

			#---------Danger Zone Length----------
			if zone.get() == "Less Dangerous":
				zoneValue = 300
			if zone.get() == "Dangerous":
				zoneValue = 500
			#-------------------------------------

			#---------Voice Assistants------------

			if voiceAssis.get() == "Alexa":
				voiceAssisName = "Alexa"

			if voiceAssis.get() == "Siri":
				voiceAssisName = "Hey Siri"

			if voiceAssis.get() == "Google":
				voiceAssisName = "Hey Google"

			if voiceAssis.get() == "Bixby":
				voiceAssisName = "Hey Bixby"

			#-------------------------------------


			if D < zoneValue and D != 0:
				frame = cv2.putText(frame, childName.get().upper()+" IS NEARER TO "+dangerName.get().upper(), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, [0, 0, 255], 4)
				engine.say(childName.get()+" IS NEARER TO"+dangerName.get())
				engine.runAndWait()
				dangerCount = dangerCount + 1
				if dangerCount >= 2:
					dangerCount = 0
					voiceCount = voiceCount + 1
					engine.say(voiceAssisName+" turn off "+dangerName.get())
					engine.runAndWait()
					if voiceCount >= 2:
						playsound.playsound('baby.wav')



			frame = cv2.putText(frame, str(D / 30) + "cm", (300, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2,
								cv2.LINE_AA)

		# show the output frame
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF

		# if the 's' key is selected, we are going to "select" a bounding
		# box to track
		if key == ord("s"):
			# select the bounding box of the object we want to track (make
			# sure you press ENTER or SPACE after selecting the ROI)
			box = cv2.selectROI("Frame", frame, fromCenter=False, showCrosshair=True)

			# create a new object tracker for the bounding box and add it
			# to our multi-object tracker
			tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()
			trackers.add(tracker, frame, box)

		# if the `q` key was pressed, break from the loop
		elif key == ord("q"):
			break

	# if we are using a webcam, release the pointer
	if not args.get("video", False):
		vs.stop()

	# otherwise, release the file pointer
	else:
		vs.release()

	# close all windows
	cv2.destroyAllWindows()


# --------------------------------------------------------------


#------------------------- GUI ---------------------------------
gui = Tk()

gui.geometry('1000x500+430+250')

gui.title("Child Danger Detection")
Label(text="Child Danger Detection", fg="black", font=('Comic Sans MS', 15)).place(x=400, y=1)

# -------- Enter Child Name ------

Label(text="Enter Child Name --->  ", font=13).place(x=100, y=100)
childName = StringVar()
Entry(gui, justify="center", textvariable=childName).place(x=350, y=100)

# --------------------------------

# -------- Enter Danger Zone Name -------

Label(text="Enter Danger Zone Name --->  ", font=13).place(x=100, y=150)
dangerName = StringVar()
Entry(gui, justify="center", textvariable=dangerName).place(x=390, y=150)
# ---------------------------------------

#-------------Danger or Less Danger--------------------

zone = StringVar()

# Dictionary with options
dangerPlaces = { 'select','Dangerous','Less Dangerous'}
zone.set('select') # set the default option

Label(gui, text="Choose Danger Type --->",font=15).place(x = 100, y = 200)
OptionMenu(gui, zone, *dangerPlaces).place(x = 345, y =198)

#------------------------------------------------------

#-------------Voice Assisstant--------------------

voiceAssis = StringVar()

Assis = { 'select','Alexa','Siri','Google','Bixby'}
voiceAssis.set('select') # set the default option

Label(gui, text="Choose Voice Assistant Type --->",font=15).place(x = 100, y = 250)
OptionMenu(gui, voiceAssis, *Assis).place(x = 400, y =248)

#------------------------------------------------------

#--------------Distraction-----------------

Button(gui, text="Distract Baby",command=distract).place(x=400, y=300)

# -----------------------------------------



# -------- Start Watching Button ---------

Button(gui, text="Start Watching",command=start_watching).place(x=400, y=400)
# ----------------------------------------


mainloop()   #tkinter function
# -------------------------------------------------------------------------------------------------------------------




