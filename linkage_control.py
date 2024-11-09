import RPi.GPIO as GPIO
import time

class Servos:

    def __init__(self):

        GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbering
        self.servo_pin1 = 17  # Example pin, update with your actual pin
        self.servo_pin2 = 27  # Example pin, update with your actual pin
        self.servo_pin3 = 22  # Example pin, update with your actual pin

        GPIO.setup(self.servo_pin1, GPIO.OUT)
        GPIO.setup(self.servo_pin2, GPIO.OUT)
        GPIO.setup(self.servo_pin3, GPIO.OUT)

        # Set frequency to 50 Hz (standard for servos)
        self.pwm1 = GPIO.PWM(self.servo_pin1, 50)
        self.pwm2 = GPIO.PWM(self.servo_pin2, 50)
        self.pwm3 = GPIO.PWM(self.servo_pin3, 50)

        self.pwm1.start(0)
        self.pwm2.start(0)
        self.pwm3.start(0)

    def set_servo_angle(self, num, angle):
        
        duty = 2 + (angle / 18)  # Map 0-180 degrees to 2-12% duty cycle

        if num == 1:
            self.pwm1.ChangeDutyCycle(duty)
        elif num == 2:
            self.pwm2.ChangeDutyCycle(duty)
        elif num == 3:
            self.pwm3.ChangeDutyCycle(duty)

        time.sleep(0.5)  # Wait for servo to reach position
        if num == 1:
            self.pwm1.ChangeDutyCycle(0)
        elif num == 2:
            self.pwm2.ChangeDutyCycle(0)
        elif num == 3:
            self.pwm3.ChangeDutyCycle(0)

    def stop_all(self):
        self.pwm1.stop()
        self.pwm2.stop()
        self.pwm3.stop()
        GPIO.cleanup()


    







