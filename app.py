# Tools this file needs.
# Flask: makes the website. jsonify: sends data as JSON.
#render_template: sends an HTML page. request: reads what the browser sent.
from flask import Flask, jsonify, render_template, request

from ai import get_steps # my own function from ai.py

app = Flask(__name__) # create the web app, tells Flask where this file lives.


# When someone visits home page ("/"), run the following function.
@app.route("/")
def home():
    return render_template("index.html") # sends the HTML page from the templates folder.

# API route: page's JS sends a task here and gets steps sent back.
# POST means the browser is sending data (the task) to the server.
@app.route("/api/breakdown", methods = ["POST"])
def breakdown():
    # Reads the JSON the broswer sent. If none, use a empty {} instead of crashing.
    data = request.get_json(silent=True) or {}
    # Pull out the task, make sure its text, and cut extra spaces
    task = str(data.get("task", "")).strip()

    # Check 1: the task can't be empty. 400 = "your request was bad"
    if task == "": # = is the task empty? if so return following.
        return jsonify({"error": "Type a task first"}), 400 # 
    # Check 2: the task can't be longer than 200 characters.
    if len(task) > 200: # = is the task too long? if so return the following.
        return jsonify({"error": "Keep your task under 200 characters."}), 400
    
    # ask the ai, if anything goes wrong, show a friendly message instead of crashing.
    try:
        steps = get_steps(task)
    except Exception as error:
        print("AI error:", error) # the real error shows in terminal to allow for debug
        # 503 = "a service (the ai) did not answer"
        return jsonify({"error": "The AI didn't answer. Try again in a minute."}), 503

    # Check: the AI has to send back at least one step
    if len(steps) == 0:
        return jsonify({"error": "The AI sent back no steps. Try rewording your task."}), 502

    # Success: send the task and steps back to the page as JSON (status 200 = Ok)
    return jsonify({"task": task, "steps": steps})

    
if __name__ == "__main__":
    app.run(debug=True) #restarts server when I save