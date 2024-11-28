from threading import Thread
import time
from server import app  # Import the app instance from server.py
from client import VideoTranslationClient

def client():
    """Start the server in a separate thread and initialize the client."""
    server_thread = Thread(target=run_server)
    server_thread.start()
    time.sleep(1)  # Wait for the server to be ready
    yield VideoTranslationClient(base_url="http://localhost:5000")  # Pass the base_url to the client
    server_thread.join()

def run_server():
    app.run(debug=True, use_reloader=False)

def test_get_status_success(mock_get):
    """
    Unit test for _get_status method when the server returns a 'completed' status.

    Args:
        mock_get (MagicMock): Mocked requests.get method.
    """
    mock_get.return_value.json.return_value = {'result': 'completed'}
    client = VideoTranslationClient()
    result = client._get_status()
    assert result == 'completed'

def test_get_status_failure(mock_get):
    """
    Unit test for _get_status method when a network error occurs.

    Args:
        mock_get (MagicMock): Mocked requests.get method.
    """
    mock_get.side_effect = requests.exceptions.RequestException("Network error")
    client = VideoTranslationClient()
    result = client._get_status()
    assert result is None

def test_check_status_timeout():
    """
    Unit test for check_status method to ensure it handles timeout properly.
    """
    client = VideoTranslationClient()
    status = client.check_status()
    assert status in ["completed", "error", "timeout"]
