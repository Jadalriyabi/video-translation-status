import pytest
from threading import Thread
from flask import Flask
import time
from client import VideoTranslationClient

# Flask server setup (as in the previous server code)

def run_server():
    app.run(debug=True, use_reloader=False)

@pytest.fixture(scope="module")
def client():
    """Start the server in a separate thread and initialize the client."""
    server_thread = Thread(target=run_server)
    server_thread.start()
    time.sleep(1)  # Wait for the server to be ready
    yield VideoTranslationClient(base_url="http://localhost:5000")
    server_thread.join()

def test_translation_status(client):
    """Test the video translation status polling with exponential backoff."""
    status = client.check_status()
    assert status in ["completed", "error"], f"Unexpected status: {status}"
