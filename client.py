import time
import requests
import logging

class VideoTranslationClient:
    def __init__(self, base_url="http://localhost:5000", max_retries=5, backoff_factor=2):
        self.base_url = base_url
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def _get_status(self):
        """Makes a GET request to the /status endpoint."""
        try:
            response = requests.get(f"{self.base_url}/status")
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json().get("result")
        except requests.RequestException as e:
            self.logger.error(f"Error fetching status: {e}")
            return None
