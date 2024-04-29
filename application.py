from flask import *
from collections import Counter
import json
import matplotlib.pyplot as plt

with open('sleeps.json', 'r') as f:
    sleep_data = json.load(f)

app = Flask(__name__)


class Global:
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    entry_mapper = {}
    SELECTED_ENTRY = ""

def get_entries():
    entries = list(Global.entry_mapper.keys())
    for _ in range(len(entries)):
        entry = entries[_].replace(" ", "_")
        entries[_] = entry
    return entries


def page_loader():
    if Global.SELECTED_ENTRY != "":
        data = sleep_data[Global.entry_mapper[Global.SELECTED_ENTRY]]
        x = data['x']
        y = data['y']
        pos = data['pos']
        m = min(len(x), len(y), len(pos))
        x = data['x'][:m]
        y = data['y'][:m]
        pos = data['pos'][:m]

        y_counts = Counter(y)
        pos_counts = Counter(pos)

        sleep_duration = len(x)
        deep_sleep_percent = y_counts[0] / sleep_duration
        restless_sleep_percent = y_counts[1] / sleep_duration
        awake_percent = y_counts[2] / sleep_duration

        left = pos_counts[0] / sleep_duration
        right = pos_counts[2] / sleep_duration
        middle = pos_counts[1] / sleep_duration

        plt.plot(x, y)
        plt.title("Sleep Quality")
        plt.xlabel("Time (seconds)")
        plt.ylabel("Restlessness Levels")
        plt.savefig("images/sleep_image.png")
        plt.clf()

        plt.plot(x, pos)
        plt.title("Sleeping Position")
        plt.xlabel("Time (seconds)")
        plt.ylabel("Left/Middle/Right")
        plt.savefig("images/pos_image.png")
        plt.clf()

        plt.pie([deep_sleep_percent, restless_sleep_percent, awake_percent], labels=["Deep Sleep", "Restless Sleep", "Awake"], autopct='%1.0f%%')
        plt.title("Sleep Efficiency")
        plt.savefig("images/sleep_efficiency_image.png")
        plt.clf()

        # get sleep_duration
        hours = sleep_duration // (60 * 60)
        sleep_duration -= hours * (60 * 60)
        minutes = sleep_duration // 60
        sleep_duration -= minutes * 60
        seconds = sleep_duration
        sleep_duration = str(hours) + " hours, " + str(minutes) + " minutes, " + str(seconds) + " seconds"

        return render_template(
            "index.html",
            sleep_data=get_entries(),
            sleep_image_path="sleep_image.png",
            pos_image_path="pos_image.png",
            sleep_efficiency_image_path="sleep_efficiency_image.png",
            sleep_duration=str(sleep_duration),
            deep_sleep_percent=str(round(deep_sleep_percent*100, 2)) + "%",
            restless_sleep_percent=str(round(restless_sleep_percent*100, 2)) + "%",
            awake_percent=str(round(awake_percent*100, 2)) + "%"
        )

    return render_template(
        "index.html",
        sleep_data=get_entries(),
        sleep_image_path="",
        pos_image_path="",
        sleep_efficiency_image_path="sleep_efficiency_image.png",
        sleep_duration="",
        deep_sleep_percent="",
        restless_sleep_percent="",
        awake_percent=""
    )

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method != "POST":
        return page_loader()
    
    clicked = request.form.get('submit_button').replace("_", " ")
    for entry in Global.entry_mapper:
        if clicked == entry:
            print(entry)
            Global.SELECTED_ENTRY = entry

    return page_loader()

@app.route('/images/<path:filename>')
def get_image(filename):
    return send_from_directory('images', filename)

if __name__ == "__main__":
    for entry in sleep_data:
        year = entry[0:4]
        month = entry[5:7]
        day = entry[8:10]
        time = entry[11:16]
        output = time + " " + Global.months[int(month)] + " " + day + ", " + year
        Global.entry_mapper[output] = entry

    app.run(debug=False, port=5000, host="192.168.1.20")