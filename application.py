from flask import *

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method != "POST":
        return render_template("index.html")
    if request.form.get("hello_button") == "Hello":
        print("hello world")
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0")