import random
import time
import logging
from flask import Flask, jsonify, render_template
from datetime import datetime, timedelta
from random import randint

app = Flask(__name__)

# Simulating delay for translation
TRANSLATION_TIME = 10

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class VideoTranslationServer:
    def __init__(self):
        delay_mins = randint(1, 5)
        self.finish_time = datetime.datetime.now() + timedelta(minutes=delay_mins)
        logging.info(f"Simulating video translation process. Time before video finishes translation: {self.finish_time}.")
        app.run(debug=True, use_reloader=False)

    @app.route('/')
    def index(self):
        """
        Renders the main UI page (index.html)
        """
        return render_template('index.html')

    @app.route('/status', methods=['GET'])
    def get_status(self):
        """
        Simulates the video translation process by introducing a random delay.
        Returns a random status (pending, completed, or error) to simulate the 
        translation process.

        Returns:
            Response (JSON): Contains the result of the translation status.
        """

        # if video has not finished processing yet
        if datetime.datetime.now() < self.finish_time:
            return jsonify({"result": "pending"})
        
        # If translation time has already passed, randomly return a result: completed, or error
        result = random.choice(["completed", "error"])
        logging.info(f"Returning translation status: {result}")

        return jsonify({"result": result})

if __name__ == '__main__':
    logging.info("Starting server...")
    server = VideoTranslationServer()
