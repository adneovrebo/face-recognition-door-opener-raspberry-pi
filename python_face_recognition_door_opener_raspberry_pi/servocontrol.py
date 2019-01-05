#Importing necessary packages
import RPi.GPIO as GPIO
from time import sleep

#Setting up the GPIO mode and the output. 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
pwm=GPIO.PWM(11, 50)
pwm.start(0)

#Function to automatically rotate to a set angle
def SetAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(11, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(11, False)
    pwm.ChangeDutyCycle(0)

#Function to close the connection with the servo
#Remember this code when closing program
def close():
    pwm.stop()
    GPIO.cleanup()
