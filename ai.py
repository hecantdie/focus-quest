# Tools needed
import os #lets python read settings, like ones in .env

from dotenv import load_dotenv # reads my secret .env key 

from google import genai # googles tool for talking to Gemini

# Read the .env file now so its values are available
load_dotenv()

# Message Im sending to the AI
# {task} is a blank that will get filled in with what the user types.
# "Put the hardest step last" is important: the last step will become the boss!
PROMPT = """Break this task into 3 to 7 small, concrete and clear steps.
Each step should take 10 to 25 minutes.
Put the hardest step last.
Reply with one step per line. No numbers, no bullets, no extra text.

Task: {task}"""


def ask_ai(task):
    """Send the task to the AI and return its reply as plain text."""
    # Fake mode: if FAKE_AI=1 in .env, skip the AI and return pretend steps.
    # This lets me Test for free. "\n" means new line.
    if os.getenv("FAKE_AI") == "1":
        return "Gather your notes\nReview chapter 3\nDo 5 practice problems\nTake a full practice test"
    # connect to googles ai using key from .env
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    # Send the prompt (with task filled in) and wait for answer
    response = client.models.generate_content(
        model=os.getenv("GEMINI_MODEL", "gemini-3.5-flash"), # which AI madel to use.
        contents=PROMPT.format(task=task), # fills the {task} blank with the real task.
    
    )
    return response.text # the AI's reply as text

def clean_line(line):
    """Tidy one line of the AI's reply(remove spaces, bullets, numbers)."""
    line = line.strip()

    if line.startswith(("-", "*", "•")):
        line = line[1:].strip()

    if line != "":
        first_word = line.split()[0]
        if first_word[:-1].isdigit() and first_word[-1] in ".)": # first_word[:-1] means "the word without its last character." "1." becomes "1". .isdigit() asks: "Is that only numbers?
            line = line[len(first_word):].strip() # len(first_word) counts the characters in "1.", which is 2.line[2:] means "everything from character 2 onward": " Gather your notes"

        return line

def parse_steps(text):
    """Turn the AI's reply into a clean list of at most 7 steps."""
    steps = [] # start with empty list
    for line in text.splitlines(): # go through the reply one line at a time
        step = clean_line(line) # cleans/tidys up the line.
        if step != "": # skips empty lines, != (not equal to).
            steps.append(step) # add the step to end of list.
    return steps[:7] # keeps only the first 7 steps

def get_steps(task):
    """Ask the AI about a task and return a clean list of steps."""
    return parse_steps(ask_ai(task)) # ask first, then clean up the response.


# This only runs when I type python ai.py (a quick way to test inside terminal)
if __name__ == "__main__":
    task = input("What are you avoiding? ") # asks me to type a task
    for step in get_steps(task):
        print("-", step) # prints each step with a dash in front.

