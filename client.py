import time
import requests
import logging
import random

class VideoTranslationClient:
    def __init__(self, base_url="http://localhost:5000", max_retries=5, backoff_factor=2, timeout=30):
        self.base_url = base_url
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.timeout = timeout

        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def _get_status(self):
        """Makes a GET request to the /status endpoint and logs the response."""
        try:
            self.logger.debug(f"Sending request to {self.base_url}/status")
            response = requests.get(f"{self.base_url}/status", timeout=self.timeout)
            response.raise_for_status()  # Raise an exception for HTTP errors
            result = response.json().get("result")
            self.logger.debug(f"Received response: {result}")
            return result
        except requests.RequestException as e:
            self.logger.error(f"Error fetching status from {self.base_url}/status: {e}")
            return None

    def check_status(self):
        """Checks the status with exponential backoff and logs every step."""
        retries = 0
        delay = 1  # Initial delay in seconds
        start_time = time.time()  # Track the start time

        self.logger.info("Starting to check the translation status...")

        while retries < self.max_retries:
            if time.time() - start_time > self.timeout:  # Check if the overall timeout has been exceeded
                self.logger.error("Timeout reached. Stopping polling.")
                return "timeout"

            self.logger.info(f"Attempt {retries + 1}/{self.max_retries} to fetch translation status...")

            result = self._get_status()

            if result == "completed":
                self.logger.info("Translation completed successfully.")
                return "completed"
            elif result == "error":
                self.logger.error("Translation failed with an error.")
                return "error"
            elif result == "pending":
                jitter = random.uniform(0, delay)  # Add jitter to the backoff time
                self.logger.info(f"Translation is still pending. Retrying in {delay + jitter:.2f} seconds...")
                time.sleep(delay + jitter)
                retries += 1
                delay *= self.backoff_factor  # Exponential backoff
            else:
                self.logger.error("Unexpected status received. Exiting.")
                return "error"

        self.logger.error("Max retries reached. Translation still pending.")
        return "error"
