from flask import Flask, jsonify
import random
import time

app = Flask(__name__)

#  Simulating delay for translation
TRANSLATION_TIME = 10  

@app.route('/status', methods=['GET'])
def get_status():
    """Simulate the video translation process."""
    # Simulate processing time
    time.sleep(random.uniform(0, TRANSLATION_TIME))  # Random delay within translation time

    # Randomly return a result: pending, completed, or error
    result = random.choice(["pending", "completed", "error"])
    return jsonify({"result": result})


if __name__ == '__main__':
    app.run(debug=True)
