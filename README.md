# harvest-net
a simple task-scheduler for web scraping

#  components:
- Task Distributor: On the main node. Its job is to distribute tasks (URLs/pages to scrape) to worker nodes:
    - Create a queue (Python's built-in queue or a list) of URLs/pages you want to scrape.
    - Have an endpoint or socket mechanism where worker nodes can request tasks.
    - Distribute tasks to nodes upon request.
- Worker Nodes: A worker node can live on the same machine as the master. Their job is to receive tasks, scrape the data, and return the results:
    - Request tasks from the Task Distributor.
    - Scrape the received URLs using tools like BeautifulSoup, Scrapy, or Requests.
    - Send the scraped data back to the Result Collector.
- Result Collector: 
    - On the master node. It gathers and stores the scraped data.
    - Have an endpoint or socket mechanism to receive scraped data.
    - Store the received data in your desired format (database, CSV, etc.).


# communication 
- Sockets
- HTTP Server

# considerations
- Error Handling:
    - Incorporate mechanisms to retry failed tasks, handle node failures, and address other issues.
- Concurrencey:
    - Use Python's threading or asyncio for concurrent task processing. This is especially important if your laptop is powerful and can handle multiple tasks simultaneously.
- Data Integrity
    - Ensure that there's no duplicate data and that all tasks are completed.
- Logging:
    -  Implement proper logging on both the distributor and worker nodes. This helps in debugging and monitoring.
- Security:
    - If using HTTP servers, consider using authentication tokens o r other methods to prevent unauthorized access.
- Task Status:
    - Maintain a record of task status (e.g., pending, in-progress, completed, failed). This aids in monitoring and recovery if needed.
- Heartbeak/Ping System:
    - Implement a mechanism where worker nodes periodically send a "heartbeat" to the main system, indicating they're active and working.

