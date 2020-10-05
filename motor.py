import RPi.GPIO as GPIO
import time

# between -90 and 90 degrees
def go_to_angle(t) :
    duty = (t + 90)/180 * 10 + 2
    pwm.ChangeDutyCycle(duty)

    time.sleep(0.5)

GPIO.setmode(GPIO.BCM)

pin = 17

GPIO.setup(pin, GPIO.OUT)
pwm = GPIO.PWM(pin, 50)

pwm.start(2.5)

go_to_angle(0)
go_to_angle(30)
go_to_angle(60)
go_to_angle(90)
go_to_angle(60)
go_to_angle(30)
go_to_angle(0)
go_to_angle(-30)
go_to_angle(-60)
go_to_angle(-90)
# go_to_angle(-60)
# go_to_angle(-30)
# go_to_angle(0)

pwm.stop()

GPIO.cleanup()
