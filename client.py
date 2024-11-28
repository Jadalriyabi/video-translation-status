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

    def check_status(self):
        """Checks the status with an exponential backoff approach."""
        retries = 0
        delay = 1  # Initial delay in seconds

        while retries < self.max_retries:
            result = self._get_status()

            if result == "completed":
                self.logger.info("Translation completed.")
                return "completed"
            elif result == "error":
                self.logger.error("Translation failed.")
                return "error"
            elif result == "pending":
                self.logger.info(f"Translation still pending. Retrying in {delay} seconds...")
                time.sleep(delay)
                retries += 1
                delay *= self.backoff_factor  # Increase the delay (exponential backoff)
            else:
                self.logger.error("Unexpected status received.")
                return "error"

        self.logger.error("Max retries reached. Translation still pending.")
        return "error"
