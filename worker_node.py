import time
from socket import socket, AF_INET, SOCK_STREAM


HOST = "localhost"
PORT = 12345
BUFFER_SIZE = 1024


def request_task():
    worker = socket(AF_INET, SOCK_STREAM)
    try:
        worker.connect((HOST, PORT))
    except ConnectionRefusedError as e:
        print(
            f"Error: Could not connect to the master node. Check the master node is running and reachable.\n{e}"
        )
        return None
    print("\nConnected to master node for task...")
    task = worker.recv(BUFFER_SIZE).decode()
    worker.close()
    return task


def send_result(task, data):
    collector = socket(AF_INET, SOCK_STREAM)
    try:
        collector.connect((HOST, PORT + 1))
    except ConnectionRefusedError as e:
        print(
            f"Error: Could not send data to the master node. Check the master node is running and reachable.\n{e}"
        )
        return
    print(f"\nSending data to master node for:\n{task}")
    collector.send(data.encode())
    collector.close()


def worker_node():
    """
    Requests a task, processes it, and sends the result back to the master node.
    """
    print("\n" + "-" * 50)
    task = request_task()

    if task == "NO_TASK":
        print("\nNo task available. Worker is idle.")
        return

    print(f"\nReceived task: \n{task}\nProcessing...")
    time.sleep(2)  # Simulating processing, actual web-scraping goes here
    scraped_data = f"Mock data from {task}"

    send_result(task, scraped_data)
    print("-" * 50 + "\n")


if __name__ == "__main__":
    worker_node()
