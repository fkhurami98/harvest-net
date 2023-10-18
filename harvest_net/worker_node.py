import socket
import time

# Constants
HOST: str = '192.168.1.121' # Change to IP of Masternode
PORT: int = 12345
BUFFER_SIZE: int = 1024

def worker_node():
    """
    Defines the functionality of a worker node.
    It requests a task, which it then processeses, then sends the result back to the master node.
    """
    print("\n" + "-"*50)
    
    # Requesting a task from the master node
    worker = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    worker.connect((HOST, PORT))
    print("\nConnected to master node for task...")
    task = worker.recv(BUFFER_SIZE).decode()
    worker.close()

    # If there's no task available, the worker remains idle
    if task == "NO_TASK":
        print("\nNo task available. Worker is idle.")
        return

    # Fake task
    print(f"\nReceived task: {task}. Processing...")
    time.sleep(2) # Simulating proccessing
    scraped_data = f"Mock data from {task}"

    # Sending processed result back to the master node
    collector = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    collector.connect((HOST, PORT + 1))
    print(f"\nSending mock data for {task} to master node...")
    collector.send(scraped_data.encode())
    collector.close()

    print("-"*50 + "\n")

worker_node()
