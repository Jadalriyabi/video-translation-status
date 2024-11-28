import random
import time
import logging
from flask import Flask, jsonify

app = Flask(__name__)

# Simulating delay for translation
TRANSLATION_TIME = 10

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/status', methods=['GET'])
def get_status():
    """
    Simulates the video translation process by introducing a random delay.
    Returns a random status (pending, completed, or error) to simulate the 
    translation process.

    Returns:
        Response (JSON): Contains the result of the translation status.
    """
    delay = random.uniform(0, TRANSLATION_TIME)
    logging.info(f"Simulating translation process with a delay of {delay:.2f} seconds.")
    time.sleep(delay)  # Simulate the translation delay

    # Randomly return a result: pending, completed, or error
    result = random.choice(["pending", "completed", "error"])
    logging.info(f"Returning translation status: {result}")

    return jsonify({"result": result})

if __name__ == '__main__':
    logging.info("Starting server...")
    app.run(debug=True, use_reloader=False)
