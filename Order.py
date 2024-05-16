import threading
import time
import random
from queue import Queue, Empty


class Worker(threading.Thread):
    def __init__(self, worker_id, resources_semaphore, should_exit):
        super().__init__()
        self.worker_id = worker_id
        self.resources_semaphore = resources_semaphore
        self.should_exit = should_exit

    def run(self):
        while not self.should_exit.is_set():
            self.resources_semaphore.acquire()
            try:
                order = order_queue.get(timeout=1)
                print(f"Worker {self.worker_id} is processing order {order}")
                time.sleep(random.randint(1, 3))

                self.resources_semaphore.release()

                order_queue.task_done()

                print(f"Worker {self.worker_id} has finished processing order {order}")

            except Empty:
                pass


class Order:
    def __init__(self, order_id, required_resources):
        self.order_id = order_id
        self.required_resources = required_resources

    def __str__(self):
        return f"{self.order_id}"


order_queue = Queue()
order_mutex = threading.Lock()
resources_semaphore = threading.Semaphore(2)
should_exit = threading.Event()

workers = []
for i in range(1, 4):
    worker = Worker(i, resources_semaphore, should_exit)
    worker.start()
    workers.append(worker)

for i in range(1, 6):
    order = Order(i, random.randint(1, 2))
    order_queue.put(order)
    print(f"Order {order} is added to the queue")

time.sleep(5)
should_exit.set()

order_queue.join()

for worker in workers:
    worker.join()
