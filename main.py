import cv2
import mediapipe as mp
import numpy as np
# import everything from folder excerises angle, curls, pushups, situps, squats
#sys append
import sys 
sys.path.append('exercises/')
from curls import curl

# open a text field userinput
userinput = input("What exercise do you want to do? ")


# if userinput is curls
if userinput == "curls":
    curl()

else: 
    print("Please enter a valid exercise")
