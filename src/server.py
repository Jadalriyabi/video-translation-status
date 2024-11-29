import random
import logging
from flask import Flask, jsonify, render_template, request
from datetime import datetime, timedelta
import uuid

app = Flask(__name__)

# Set up logger with consistent format
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class VideoTranslationServer:
    def __init__(self):
        delay_mins = random.randint(1, 5)
        self.finish_time = datetime.now() + timedelta(minutes=delay_mins)
        
        # Set up instance-specific logger
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Simulating video translation process. Time before video finishes translation: {self.finish_time}.")
        
        # Initialize an empty dictionary to store video metadata
        self.video_data = {}

    def start_translation(self, video_name, video_length):
        """
        Starts a new video translation process.
        """
        # Generate a unique video identifier
        video_identifier = str(uuid.uuid4())  # Unique video identifier

        # Simulate random delay in translation start
        delay_mins = random.randint(1, 5)
        finish_time = datetime.now() + timedelta(minutes=delay_mins)

        video_data = {
            "video_name": video_name,
            "video_identifier": video_identifier,
            "video_length": video_length,  # In seconds
            "translation_progress": 0,
            "status": "pending",  # Initial status is "pending"
            "timestamp": datetime.now().isoformat(),
            "finish_time": finish_time.isoformat()
        }

        # Store video data in the server's memory (simulated DB)
        self.video_data[video_identifier] = video_data

        logging.info(f"Started translation for {video_name} (ID: {video_identifier}). Will finish at {finish_time}.")
        
        return video_identifier, finish_time

# Instantiate the server object
video_translation_server = VideoTranslationServer()


@app.route('/')
def index():
    """
    Renders the main UI page (index.html)
    """
    return render_template('index.html')


@app.route('/status', methods=['GET'])
def get_status():
    """
    Returns the status of a video translation.
    If video not found, returns 404.
    """
    video_identifier = request.args.get('video_identifier')

    if video_identifier not in video_translation_server.video_data:
        logging.error(f"Video with identifier {video_identifier} not found.")
        return jsonify({"error": "not_found"}), 404

    # Retrieve the video data from the simulated database
    video_data = video_translation_server.video_data[video_identifier]

    # If video has not finished processing yet
    if datetime.now() < datetime.fromisoformat(video_data["finish_time"]):
        return jsonify({"result": "pending"})
    
    # If translation time has already passed, randomly return a result: completed, or error
    result = random.choice(["completed", "error"])
    video_translation_server.logger.info(f"Returning translation status: {result}")

    return jsonify({"result": result})


@app.route('/translate_video_api', methods=['POST'])
def translate_video_api():
    """
    Initiates the translation of a new video.
    Takes the video name and length as input and starts the translation process.
    """
    data = request.get_json()

    if not data or 'video_name' not in data or 'video_length' not in data:
        return jsonify({"error": "Invalid input, missing 'video_name' or 'video_length'."}), 400

    # Start video translation
    video_identifier, finish_time = video_translation_server.start_translation(
        data["video_name"], data["video_length"]
    )

    return jsonify({
        "message": f"Video '{data['video_name']}' translation started.",
        "video_identifier": video_identifier,
        "finish_time": finish_time.isoformat()
    }), 202


if __name__ == '__main__':
    logging.info("Starting server...")
    app.run(debug=True, use_reloader=False)
