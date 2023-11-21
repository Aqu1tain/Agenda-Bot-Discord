from flask import Flask, render_template
from threading import Thread

app = Flask(__name__)

@app.route('/')
def index():
    """
    A function that serves as the handler for the root URL ("/") of the application.

    Returns:
        str: A string indicating that the server is alive.
    """
    return "Alive"

def run():
    """
    Run the application on the specified host and port.

    Parameters:
    - host (str): The host to run the application on. Defaults to '0.0.0.0'.
    - port (int): The port to run the application on. Defaults to 8080.
    """ 
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    """
    Start a new thread to keep the program alive.
    """
    t = Thread(target=run)
    t.start()