import socket
import threading
from queue import Queue

# Constants
HOST: str = '0.0.0.0'
PORT: int = 12345
BUFFER_SIZE: int = 1024

URLS: list = [
    "http://example.com/news1",
    "http://example.com/news2",
    "http://example.com/news3",
]

# Instintaniate a task_queue using the Queue() class
task_queue = Queue()

# Populating the task queue
for url in URLS:
    task_queue.put(url)

# Instintaniate a empty result list
results = []


def task_distributor():
    """
    This function listens for worker connections and distributes tasks to them.
    """
    distributor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    distributor.bind((HOST, PORT))
    distributor.listen(5)
    print("Master node started, waiting for worker connections...\n" + "-"*50)

    while True:
        worker, addr = distributor.accept()
        print(f"\nConnected to worker @ {addr}")
        if not task_queue.empty():
            task = task_queue.get()
            print(f"\nSending task: {task} to worker @ {addr}")
            worker.send(task.encode())
        else:
            print("\nNo tasks available. Sending 'NO_TASK' message to worker.")
            worker.send("NO_TASK".encode())
        worker.close()


def result_collector():
    """
    This function listens for results from workers and collects them.
    """
    collector = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    collector.bind((HOST, PORT + 1))
    collector.listen(5)
    print("\nResult collector started, waiting for results...\n" + "-"*50)

    while True:
        worker, addr = collector.accept()
        data = worker.recv(BUFFER_SIZE).decode()
        if data != "NO_TASK":
            results.append(data)
            print(f"\nReceived data from worker @ {addr}: {data}")
        worker.close()


# Starting the distributor and collector threads
threading.Thread(target=task_distributor).start()
threading.Thread(target=result_collector).start()

# Keeping the script running for testing purposes
try:
    while True:
        pass
except KeyboardInterrupt: # Ctrl + C to see results.
    print("\nResults collected:", results)
