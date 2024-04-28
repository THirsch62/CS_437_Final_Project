import time

from utils import *

setup_board()

while True:
    print("Sensor 1:", sensor(1))
    print("Sensor 2:", sensor(2))
    print("Sensor 3:", sensor(3))
    print("Sensor 4:", sensor(4))