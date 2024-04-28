import RPi.GPIO as GPIO

# set vibration sensor channels
SENSOR_1 = 2
SENSOR_2 = 3
SENSOR_3 = 4
SENSOR_4 = 14
SENSORS = {
    1: SENSOR_1,
    2: SENSOR_2,
    3: SENSOR_3,
    4: SENSOR_4
}

def setup_board():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SENSOR_1, GPIO.IN)
    GPIO.setup(SENSOR_2, GPIO.IN)
    GPIO.setup(SENSOR_3, GPIO.IN)
    GPIO.setup(SENSOR_4, GPIO.IN)

def sensor(val):
    return GPIO.input(SENSORS[val])

def pillow_in_use():
    return False

