# Video Translation Client & Server

This project simulates a video translation system. The server provides a status API that returns whether the translation process is "pending", "completed", or "error". The client library allows third-party users to check the status of the translation job, using an exponential backoff approach for retrying.

---

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Running the Server](#running-the-server)
- [Using the Client](#using-the-client)
- [Running Tests](#running-tests)
- [Dockerization](#dockerization)
- [Usage Example](#usage-example)
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



   
