from flask import Flask, render_template
from swiper_GUI import GUI

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/instructions")
def instructions():
    return render_template("instructions.html")

@app.route("/collect")
def collect():
    return GUI()

if __name__ == "__main__":
    app.run(debug=True)
