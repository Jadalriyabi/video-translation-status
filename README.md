# video-translation-status
Simulateing a video translation service with a backend server that returns job status (pending, completed, error). The client library intelligently polls the server using backoff to minimize load while tracking translation progress. Includes tests and detailed logging.
