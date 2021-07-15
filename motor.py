import RPi.GPIO as GPIO
import time
import sys

# between -90 and 90 degrees
def go_to_angle(t) :
    duty = (t + 90.0)/180 * 10 + 2
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)

if (len(sys.argv) < 2) :
    print(sys.argv[0] + ' angle')
    sys.exit(0)

angle = float(sys.argv[1])

GPIO.setmode(GPIO.BCM)

pin = 4

GPIO.setup(pin, GPIO.OUT)
pwm = GPIO.PWM(pin, 50)

pwm.start(2.5)

print('Go to angle ' + str(angle))
go_to_angle(angle)

pwm.stop()

GPIO.cleanup()
