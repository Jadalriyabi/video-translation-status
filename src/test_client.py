import pytest
import time
import logging
import requests
from unittest.mock import patch
from server import app  # Import the app instance from server.py
from client import VideoTranslationClient

# Set up logger for test logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Helper function to wait for the server to be ready
def wait_for_server(url, timeout=10):
    """Wait for the server to start by polling the given URL."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                logger.info("Server is ready.")
                return
        except requests.ConnectionError:
            pass  # Keep trying if the connection fails
        time.sleep(1)
    raise Exception(f"Server at {url} did not start within {timeout} seconds.")

# Client fixture to start server and initialize client
@pytest.fixture
def client():
    """Start the server in a separate thread and initialize the client."""
    server_thread = Thread(target=run_server)
    server_thread.start()

    # Wait for the server to be ready by checking the /status endpoint
    wait_for_server("http://localhost:5000/status")

    yield VideoTranslationClient(base_url="http://localhost:5000")  # Pass the base_url to the client

    server_thread.join()

# Function to run Flask app in a separate thread
def run_server():
    app.run(debug=True, use_reloader=False)

# Test for _get_status method when server returns 'completed' status
@patch('requests.get')
def test_get_status_success(mock_get, client):
    """
    Unit test for _get_status method when the server returns a 'completed' status.
    """
    # Mocking the server response
    mock_get.return_value.json.return_value = {'result': 'completed'}
    logger.info("Testing _get_status success.")
    
    result = client._get_status()
    logger.info(f"Received result: {result}")
    
    assert result == 'completed'

# Test for _get_status method when network error occurs
@patch('requests.get')
def test_get_status_failure(mock_get, client):
    """
    Unit test for _get_status method when a network error occurs.
    """
    # Simulating network error
    mock_get.side_effect = requests.exceptions.RequestException("Network error")
    logger.error("Testing _get_status failure due to network error.")
    
    result = client._get_status()
    logger.error(f"Received result: {result}")
    
    assert result is None

# Test for check_status method to ensure it handles timeout properly
@patch('requests.get')
def test_check_status_timeout(mock_get, client):
    """
    Unit test for check_status method to ensure it handles timeout properly.
    """
    # Simulating retry behavior (e.g., return "pending" for 2 tries then timeout)
    mock_get.return_value.json.return_value = {'result': 'pending'}
    logger.info("Testing check_status timeout handling.")
    
    status = client.check_status()
    logger.info(f"Final status: {status}")
    
    assert status == "timeout"  # Expect timeout after retries

# Test for check_status method when translation is successful
@patch('requests.get')
def test_check_status_success(mock_get, client):
    """
    Unit test for check_status when the translation is completed.
    """
    # Simulate server returning 'pending' twice and then 'completed'
    mock_get.return_value.json.return_value = {'result': 'pending'}
    
    # First two attempts return 'pending'
    result = client._get_status()
    logger.info(f"Attempt 1: {result}")
    result = client._get_status()
    logger.info(f"Attempt 2: {result}")
    
    # Third attempt returns 'completed'
    mock_get.return_value.json.return_value = {'result': 'completed'}
    result = client._get_status()
    logger.info(f"Attempt 3: {result}")
    
    # Now check for success
    status = client.check_status()
    logger.info(f"Final status: {status}")
    
    assert status == "completed"

# Test for check_status method when translation fails
@patch('requests.get')
def test_check_status_error(mock_get, client):
    """
    Unit test for check_status when the translation has an error.
    """
    # Simulate server returning 'pending' twice and then 'error'
    mock_get.return_value.json.return_value = {'result': 'pending'}
    
    # First two attempts return 'pending'
    result = client._get_status()
    logger.info(f"Attempt 1: {result}")
    result = client._get_status()
    logger.info(f"Attempt 2: {result}")
    
    # Third attempt returns 'error'
    mock_get.return_value.json.return_value = {'result': 'error'}
    result = client._get_status()
    logger.info(f"Attempt 3: {result}")
    
    # Now check for error
    status = client.check_status()
    logger.error(f"Final status: {status}")
    
    assert status == "error"

# Test for server startup and client interaction
@pytest.mark.parametrize("video_name, video_length", [
    ("Test Video 1", 120),
    ("Test Video 2", 60),
    ("Test Video 3", 180)
])
def test_server_interaction(client, video_name, video_length):
    """
    Test for video translation initiation and status checks.
    """
    logger.info(f"Testing video translation for {video_name} of {video_length} seconds.")
    
    # Initiate translation via the API
    response = client.translate_video_api(video_name, video_length)
    logger.info(f"Translation started: {response['message']}")
    
    # Fetch the video identifier and expected finish time from the response
    video_identifier = response['video_identifier']
    expected_finish_time = response['finish_time']
    
    # Check status of video translation
    status = client.check_status(video_identifier)
    logger.info(f"Translation status: {status}")
    
    assert status in ["completed", "error", "timeout"]

