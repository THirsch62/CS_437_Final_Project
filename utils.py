import RPi.GPIO as GPIO
import time
import numpy as np

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

def get_current_state():
    sens1, sens2 = [], []
    end = time.time() + 1
    while time.time() <= end:
        sens1.append(sensor(1))
        sens2.append(sensor(2))
    current_state = (np.average(sens1), np.average(sens2))
    print(current_state)
    return current_state

