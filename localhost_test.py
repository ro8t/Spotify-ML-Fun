# Dependencies..imports
from flask import Flask, jsonify

# Flask localhost setup

test_host = Flask(__name__)

# Flask routes

welcome_message = ["Welcome to my local server!",
                   "The following api routes are available in this test scenario:",
                   "    1. /about",
                   "    2. /objectives"]

@test_host.route("/")
def landing():
    print("Home/Landing page reached")
    return jsonify(welcome_message)

about_message = [
    {"Name/Author": "Rohan Bh."},
    {"Education": ["University of Illinois at Urbana-Champaign (UIUC)",
                    "University of California at Berkeley (UCB)"]},
    {"Degrees": ["UIUC: Bachelors Degree in Economics, Game Theory",
                "UCB: Bootcamp Certificate in Data Analytics"]},
    {"Hometown": "San Francisco Bay Area"}
]

@test_host.route("/about")
def about():
    print("About page reached")
    return jsonify(about_message)


objective_message = [f"The main purpose of this project is to push my coding and machine learning skills to the"
                     f" limit. I love exploring and finding new music, analyzing the world of music is just my"
                     f" next step in my music exploration."]

@test_host.route("/objectives")
def objectives():
    print("Objectives page reached")
    return jsonify(objective_message)

# Running host

if __name__ == "__main__":
    test_host.run(debug=True)