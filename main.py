import matplotlib.pyplot as plt
import json
import datetime

from utils import *

setup_board()

MAX_AWAKE_TIME = 10 #60 * 15
AWAKE_SET = set([2])

def pillow_in_use(state):
    return (state[0] > .5) or (state[1] > .5)

def potential_disturbance(sleep):
    if len(sleep) < MAX_AWAKE_TIME:
        return True
    
    if set(sleep[-MAX_AWAKE_TIME:]) == AWAKE_SET:
        return False

    return True

with open('sleeps.json', 'r') as f:
    sleep_data = json.load(f)

try:
    while True:
        current_state = get_current_state()
        x, y = [], []   # y: 0=deep sleep, 1=restless sleep, 2=awake
        pos = []        # 0=right, 1=middle, 2=left
        t = 0

        if not pillow_in_use(current_state):
            continue

        while pillow_in_use(current_state) or potential_disturbance(y):
            next_state = get_current_state()
            left, right = abs(next_state[0] - current_state[0]), abs(next_state[1] - current_state[1])

            x.append(t)
            t += 1

            if (next_state[0] < 0.05) and (next_state[1] < 0.05):   # awake
                y.append(2)
            elif left + right < 0.2:                            # deep sleep
                y.append(0)
            else:                                               # restless sleep
                y.append(1)

            if (next_state[0] > 0.5) and (next_state[1] < 0.5):
                pos.append(0)
            elif (next_state[0] < 0.5) and (next_state[1] > 0.5):
                pos.append(2)
            else:
                pos.append(1)

            current_state = next_state
        
        x, y = x[:-MAX_AWAKE_TIME], y[:-MAX_AWAKE_TIME]

        current_sleep_data = {
            'x': x,
            'y': y,
            'pos': pos,
        }

        sleep_data[str(datetime.datetime.now())] = current_sleep_data

        plt.plot(x, y)
        plt.savefig("sleep.png")

except:
    with open('sleeps.json', 'w') as f:
        json.dump(sleep_data, f)
