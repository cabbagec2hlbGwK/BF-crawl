# Application Setup Guide

## Architecture Overview

This application consists of two main components:

1. **AgentHandler**: This component is responsible for:

   - Creating agents and maintaining their states.
   - Restarting agents if something goes wrong.
   - Distributing tasks and determining which pages to crawl.
   - Managing the task pipeline to ensure smooth operation.

2. **ApplicationHandler**: This component handles:

   - Providing core functionalities like solving captchas.
   - Managing other related operations required for the application.

Together, these components work seamlessly to ensure the application runs efficiently and handles its tasks effectively.

## What You Need

Before you start, make sure you have these installed:

- [Docker](https://www.docker.com/) - A tool to run applications in containers
- [Docker Compose](https://docs.docker.com/compose/) - Helps manage multiple Docker containers
- The right environment variables set up for this app

## How to Run the App

### Step 3: Clone the Repository and Build the Agent Image

1. Open a terminal and clone the repository:
   ```bash
   git clone https://github.com/cabbagec2hlbGwK/BF-crawl-.git && cd BF-crawl
   ```
2. Navigate to the `agent` folder:
   ```bash
   cd agent
   ```
3. Build the Docker image for the agent:
   ```bash
   docker build -t bf-agent .
   ```

### Step 2: Build the Master Image

1. Go back to the main folder:
   ```bash
   cd ..
   ```
2. Build the Docker image for the master:
   ```bash
   docker build -t bf-master .
   ```

### Step 3: Run the App Using Docker Compose

1. Make sure the following environment variables are set up:

   - `OPENAI_API_KEY`: Your OpenAI API key
   - `ELASTIC_API`: The API endpoint for Elasticsearch
   - `ELASTIC_HOST`: The address of your Elasticsearch server
   - `ELASTIC_INDEX`: The name of your Elasticsearch index
   - `BF_CREDS`: Credentials for the BF system. The format for these credentials should look like this:
     ```json
     [
       {"username1": "password1"},
       {"username2": "password2"},
       {"username3": "password3"}
     ]
     ```

   You can set these in your terminal or create an `.env` file to load them automatically.

2. Start the app with Docker Compose:
   ```bash
   docker-compose -f deploy.yaml up
   ```

### Step 4: Check If Everything Works

1. Check if the `masternode` container is running by listing all running containers:
   ```bash
   docker ps
   ```
2. Look at the app logs to see if it started successfully.

## Common Problems and Fixes

- **Missing Environment Variables:** Make sure all required variables are set before running the app.
- **Docker Issues:** Ensure Docker is installed, running, and working correctly on your system.
- **Port Problems:** Check that no other programs are using the ports the app needs.

---


