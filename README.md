# Video Translation Client & Server

This project simulates a video translation system. The server provides a status API that returns whether the translation process is "pending", "completed", or "error". The client library allows third-party users to check the status of the translation job, using an exponential backoff approach for retrying.

---

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Running the Server](#running-the-server)
- [Running the Client](#running-the-client)
- [Running with Docker](#running-with-docker)
- [Usage Example](#usage-example)
- [Testing](#testing)
- [Features](#features)
- [License](#license)

---

## Overview

Heygen is an AI-powered video creation platform, and one of its features is video translation with lip-sync. When users translate videos from one language to another, it can be a time-consuming process depending on video length and other factors.

This project simulates the backend of the translation process with a status API that provides information about the current state of a video translation (either "pending", "completed", or "error").

You will also find a client library that interacts with this server, implementing **exponential backoff** for polling status, making the client efficient in terms of the number of requests made.

---

## Project Structure

The project is divided into the following main components:
```
/video-translation/ 
    ├── server.py # Simulated server that provides translation status 
    ├── client.py # Client library to interact with the server 
    ├── cli.py # Command-line tool to check translation status 
    ├── test_client.py # Unit and integration tests 
    ├── Dockerfile # Docker file to containerize the project 
    ├── docker-compose.yml # Docker Compose configuration for running both client and server 
    ├── requirements.txt # Python dependencies 
    └── README.md
```



---

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone https://github.com/yourusername/video-translation.git
   cd video-translation
   ```

2. **Create and activate a virtual environment (optional but recommended):**
   ```
   python3 -m venv venv
   source venv/bin/activate   # For Mac/Linux
   venv\Scripts\activate      # For Windows
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Run the server (in one terminal):**
    ```
    python server.py
    ```
This will start the Flask server on http://localhost:5000.


---

## Running the Client

To run the client, you can either use the command line interface (CLI) or run it directly in a script. Here's how to use the client to check the translation status:

1. **Run the Client:**
In another terminal, you can run the client to start checking the translation status:
```
python client.py
```
This will check the status of the translation at regular intervals and log the results.

---

## Running with Docker
To make it easier to run the server and client in a production-like environment, we’ve included Docker support.

1. **Build and start the containers using Docker Compose:**
```
docker-compose up --build
```
This will start both the server and client in separate containers, with the server accessible at http://localhost:5000 and the client running in the background checking the translation status.

2. **Stop the containers:**
```
docker-compose down
```

---


## Usage Example
Here’s an example of how the client interacts with the server.

1. **Run the server (from one terminal):**

```
python server.py
```
This starts the server on http://localhost:5000.

2. **Run the client (from another terminal):**

```
python client.py
```
The client will:

- Query the /status endpoint at regular intervals.
- Retry with exponential backoff if the status is pending.
- Stop retrying if the translation is completed or error.

```
2024-11-28 12:30:00 - INFO - Starting to check the translation status...
2024-11-28 12:30:01 - INFO - Attempt 1/5 to fetch translation status...
2024-11-28 12:30:03 - INFO - Translation is still pending. Retrying in 2.32 seconds...
2024-11-28 12:30:05 - INFO - Attempt 2/5 to fetch translation status...
2024-11-28 12:30:06 - INFO - Translation completed successfully.
```

---


## Testing

I've included unit tests and integration tests using pytest.

1. **Run the tests:**
```
pytest
```
This will run the tests, including:

- Testing the exponential backoff logic in the client.
- Simulating various server responses (pending, completed, error) using mock data.
- Ensuring the client correctly handles retries, timeouts, and errors.

2. **Test Client:**
test_client.py
```
def test_translation_status(client):
    """Test the video translation status polling with exponential backoff."""
    status = client.check_status()
    assert status in ["completed", "error"], f"Unexpected status: {status}"
```

---

## Features


**Server Simulations:**

The server responds with a randomized status (pending, completed, or error).
Configurable maximum translation delay via the TRANSLATION_TIME variable.

**Exponential Backoff in Client:**

The client retries the request using an exponential backoff strategy, with an optional jitter to avoid synchronization issues between clients.

**Docker Support:**

Containerized both the server and client for easy deployment using docker-compose.
Configurable parameters (e.g., retries, timeout) can be passed via environment variables.

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.
