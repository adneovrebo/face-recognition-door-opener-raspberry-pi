#Ådne Øvrebø 2019

# import the necessary packages for the face recognition
import face_recognition
import argparse
import pickle
import cv2
import sys

# import the necessary packages for the camera
from picamera.array import PiRGBArray
from picamera import PiCamera
from time import sleep
# Import the necessary self created functions
import door
import servocontrol #Maybe not nesesarry to import

try:
    #Setting up the camera
    camera = PiCamera()
    #Choosing the resolution of the picture, lower resolution gives lower prosessing time.
    camera.resolution = (250, 250)
    #Initialising the capture.
    rawCapture = PiRGBArray(camera)
    #Capturing the first initialising picture.
    camera.capture(rawCapture, format="bgr")

    # load the known faces and embeddings
    print("[INFO] loading encodings...")
    data = pickle.loads(open("/home/pi/Desktop/face-recognition-door-opener-raspberry-pi/encodings.pickle", "rb").read())
    
    nrunknown = 0
    
    #Running all the time untill terminated
    #while True:
    def recogniceFaces():
        #Taking a picture.
        rawCapture = PiRGBArray(camera)
        camera.capture(rawCapture, format="bgr")
        print("Tar bilde")
        image = rawCapture.array
        
        #Keeps track of a person is approved or not.
        approved = False
        
        # load the input image and convert it from BGR to RGB
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # detect the (x, y)-coordinates of the bounding boxes corresponding
        # to each face in the input image, then compute the facial embeddings
        # for each face
        print("[INFO] recognizing faces...")
        boxes = face_recognition.face_locations(rgb,
            model="hog") #You can use hog or cnn. (hog is faster)
        encodings = face_recognition.face_encodings(rgb, boxes)

        # initialize the list of names for each face detected
        names = []

        # loop over the facial embeddings
        for encoding in encodings:
            # attempt to match each face in the input image to our known
            # encodings
            matches = face_recognition.compare_faces(data["encodings"],
                encoding)
            name = "Unknown" #Putting the name to unknown if the person is not recognised.

            # check to see if we have found a match
            if True in matches:
                # find the indexes of all matched faces then initialize a
                # dictionary to count the total number of times each face
                # was matched
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}

                # loop over the matched indexes and maintain a count for
                # each recognized face face
                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1

                    #Approving the persons
                    if (name == "adne_ovrebo" or name == "amalie_eikeskog") and approved == False:
                        print("Approved") #Print to the terminal that the person is approved
                        approved = True #Telling the program the person is approved.
                        door.unlock() #If it gets approved two times the door unlocks.

                # determine the recognized face with the largest number of
                # votes (note: in the event of an unlikely tie Python will
                # select first entry in the dictionary)
                name = max(counts, key=counts.get)
            else:
                print("Ikke godkjent")
                global nrunknown
                nrunknown = nrunknown + 1
                #saving the unknown persons to the unknown folder
                cv2.imwrite("/home/pi/Desktop/face-recognition-door-opener-raspberry-pi/unknown/unknown" + str(nrunknown) + ".jpg", image)
            
            # update the list of names
            names.append(name)

        # loop over the recognized faces
        for ((top, right, bottom, left), name) in zip(boxes, names):
            # draw the predicted face name on the image
            cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                0.75, (0, 255, 0), 2)

        # show the output image
        #cv2.imshow("Image", image)
        #cv2.waitKey(1)
        #Terminating the camerastream
        rawCapture.truncate(0)
        cv2.imwrite("/home/pi/Desktop/face-recognition-door-opener-raspberry-pi/lastimage/lastimage.jpg", image)

        
        #Locks the door after x seconds if the dor opens
        if approved == True:
            #Number of second before the door locks ofter opening
            sleep(10)
            #Locking the door
            door.lock()
            return "Opened and closed door for owner."
            
except KeyboardInterrupt:
    servocontrol.close()
    print("The program has been terminated")
    
