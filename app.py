# ---...---...---...---...---...---...---...---...---...---...---...---...---
#
#                    HOW TO BUILD THIS APPLICATION
#
# 1. SETUP & INSTALLATION:
#    Open your terminal or command prompt and install the necessary libraries.
#
#    pip install pywebview
#    pip install pyinstaller
#
# 2. FILE STRUCTURE:
#    Make sure this Python script (e.g., app.py) is in the SAME folder as your
#    web files:
#    - index.html
#    - style.css
#    - script.js
#
# 3. CREATE THE .EXE FILE:
#    Navigate to your project folder in the terminal and run the following
#    command. This command bundles everything into a single executable file.
#
#    pyinstaller --onefile --windowed --add-data "index.html:." --add-data "style.css:." --add-data "script.js:." app.py
#
#    COMMAND BREAKDOWN:
#    --onefile   : Creates a single .exe file.
#    --windowed  : Hides the black command prompt window when your app runs.
#    --add-data  : Includes your web files in the application bundle.
#    app.py      : The name of this Python script.
#
# 4. RUN YOUR APPLICATION:
#    After the command finishes, look inside the newly created 'dist' folder.
#    You will find your 'app.exe' file there. You can now run it.
#
# ---...---...---...---...---...---...---...---...---...---...---...---...---


import webview
import threading
import time
import os
import sys # Import sys

# Get the directory of the current script
# This is crucial for Pywebview to find the HTML, CSS, and JS files
script_dir = os.path.dirname(os.path.abspath(__file__))
html_file_path = os.path.join(script_dir, 'index.html')

# Define a simple API class to expose Python functions to JavaScript
class Api:
    def __init__(self, window=None): # Changed to allow initialization with None
        self.window = window
        self.js_ready = False

    # This function is called from JavaScript (e.g., by the button click)
    def say_hello_from_python(self, name):
        print(f"Python received a call from {name}!")
        return f"Hello, {name}! This message is from Python."

    # This function is called from JavaScript to signal that JS is ready
    def init_js_ready(self):
        self.js_ready = True
        print("JavaScript is ready!")
        # Once JS is ready, we can call a JS function from Python
        # We'll do this in a separate thread to avoid blocking the main thread
        threading.Thread(target=self.call_js_after_delay).start()

    # A function to demonstrate calling JavaScript from Python after a delay
    def call_js_after_delay(self):
        # Wait until JS is confirmed ready
        while not self.js_ready:
            time.sleep(0.1) # Small delay to prevent busy-waiting
        
        time.sleep(2) # Simulate some work or a delay
        message_from_python = "Python is now updating the message in JavaScript!"
        print(f"Python is calling JavaScript with: '{message_from_python}'")
        # Call the 'updateMessage' JavaScript function
        # The `evaluate_js` method is used to execute JavaScript code in the webview
        self.window.evaluate_js(f"updateMessage('{message_from_python}')")

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def main():
    # Use the new helper function to define file paths
    html_file_path = resource_path('index.html')

    api = Api()

    window = webview.create_window(
        'Pywebview HTML/CSS/JS Demo',
        url=f'file://{html_file_path}', # Use the robust path
        min_size=(600, 400),
        js_api=api
    )
    
    api.window = window

    webview.start(debug=False) # Set debug to False for final build

if __name__ == '__main__':
    main()