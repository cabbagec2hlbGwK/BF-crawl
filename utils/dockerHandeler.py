import docker

def create_and_run_container():
    # Initialize the Docker client
    client = docker.from_env()

    try:
        # Create the container
        container = client.containers.run(
            image="agent4",  # Replace with your image
            detach=True,  # Run in detached mode
            name="app",  # Optional: container name
            network="myapp",  # Attach to the existing network
            environment={
                "MASTER": "http://agent1:5000"

                    },  # Set environment variables
        )
        print(f"Container {container.name} created and running.")
    except docker.errors.APIError as e:
        print(f"Error: {e.explanation}")

if __name__ == "__main__":
    create_and_run_container()

