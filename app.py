# Bringing in the Flask tool so the file can create a web app.
from flask import Flask

app = Flask(__name__) # create the web app, tells Flask where this file lives.


# When someone visits home page ("/"), run the following function.
@app.route("/")
def home():
    return "This is Focus Quest AI" # Whatever this function returns is what the browser shows.

@app.route("/about")
def about():
    return "This is what AI Focus Quest is About"


if __name__ == "__main__":
    app.run(debug=True)