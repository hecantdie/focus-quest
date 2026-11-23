// -- Elements on the page --
// Find each box on the page by its id and keep it in a variable
const form = document.getElementById("task-form"); // the form (box + button)
const taskInput = document.getElementById("task-input"); // text box
const message = document.getElementById("message"); // where messages show
const stepList = document.getElementById("step-list"); // the empty list for steps

// Puts any text into the message spot under the box
function showMessage(text) {
    message.textContent = text;
}

// Temp version: Will replace later.
// Shows each step as an item in list
function startQuest(task, stepTexts) {
    stepList.innerHTML = ""; // empty list first
    for (const text of stepTexts) {
        const item = document.createElement("li"); // make a new list item.
        item.textContent = text; // put the step's words in it 
        stepList.appendChild(item); // adds it to page 
    }
}

// Sections: Asking the server for steps
// When the form is submitted (button click or Enter), runs this code.
form.addEventListener("submit", async (event) => {
    event.preventDefault(); // stops browser from reloading the page
    const task = taskInput.value.trim(); // what user typed, no extra spaces
    if (task === "") {
        showMessage("Type a task first.");
        return; // stops here
    }

    showMessage("Breaking it down...");
    try {
        // sends the task to my Flask route and waits for answer.
        const response = await fetch("/api/breakdown", {
            method: "POST", // POST = Im sending data
            headers: { "Content-Type": "application/json"}, // data is JSON
            body: JSON.stringify({ task: task }), // turn data to JSON text
        });
        const data = await response.json(); // turns the JSON answer back into data
        if (!response.ok) {
            showMessage(data.error); // server said something was wrong
            return;
        }
        showMessage("");
        startQuest(data.task, data.steps); // success: shows the steps
    } catch (error) {
        // Server couldn't be reached at all
        showMessage("Couldn't reach the server. Is it running?");
    }
});
