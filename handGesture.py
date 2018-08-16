import cv2
import numpy as np
import math

import os
import winsound

n = 1
sound_directory = os.listdir("G:/Work/OP/audio")
print sound_directory
sound_track = []
for song in sound_directory:
	if song.endswith('.wav'):
		sound_track.append(song)
print sound_track
i = 0
flag = 0
winsound.PlaySound(None, winsound.SND_PURGE)

cap = cv2.VideoCapture(0)

while (1):
	
	ret, frame = cap.read()
	frame = cv2.flip(frame,1)
	kernel = np.ones((3,3),np.uint8)

	roi = frame[100:300, 100:300]
	cv2.rectangle(frame,(100,100),(300,300),(0,255,0),0)    
	hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

	cv2.imshow('hsv', hsv)

	lower_glove = np.array([0,0,235], dtype=np.uint8)  # 65,0,160
	upper_glove = np.array([180,255,255], dtype=np.uint8)

	mask = cv2.inRange(hsv, lower_glove, upper_glove)
	cv2.imshow('initial mask', mask)

	mask = cv2.dilate(mask, kernel, iterations = 4)
	mask = cv2.GaussianBlur(mask,(3,3),100)

	_,contours,hierarchy= cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	cnt = max(contours, key = lambda x: cv2.contourArea(x))
	epsilon = 0.0005*cv2.arcLength(cnt,True)
	approx= cv2.approxPolyDP(cnt,epsilon,True)

	hull = cv2.convexHull(cnt)
	areahull = cv2.contourArea(hull)
	areacnt = cv2.contourArea(cnt)
	arearatio=((areahull-areacnt)/areacnt)*100
	hull = cv2.convexHull(approx, returnPoints=False)
	defects = cv2.convexityDefects(approx, hull)

	font = cv2.FONT_HERSHEY_SIMPLEX
	print (len(defects))
	if len(defects) > 12:
		cv2.putText(frame,'Play',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
		if flag==0:
			flag = 1
			winsound.PlaySound(r"G:/Work/OP/audio/"+sound_track[i], winsound.SND_ASYNC)
	else:
		cv2.putText(frame,'Pause',(0,50), font, 2, (0,0,255), 3, cv2.LINE_AA)
		if flag==1:
			flag = 0
			winsound.PlaySound(None, winsound.SND_PURGE)

	

	cv2.imshow('mask', mask)
	cv2.imshow('frame', frame)

	k = cv2.waitKey(5) & 0xFF
	if k == 27:
		break

cv2.destroyAllWindows()
cap.release()  