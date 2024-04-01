from queue import Queue
from threading import Thread, Event
import time
import os
from jobs import Job

class ThreadPool:
    def __init__(self):
        self.jobs = Queue()
        self.nr_threads = os.getenv("TP_NUM_OF_THREADS", os.cpu_count())
        self.threads = [TaskRunner(self) for _ in range(self.nr_threads)]

    def add_job(self, job : Job):
        self.jobs.put(job)

    def get_job(self) -> Job:
        return self.jobs.get()
    

class TaskRunner(Thread):
    def __init__(self, pool : ThreadPool):
        super.__init__(self)
        self.pool = pool

    def run(self) -> None:
        while True:
            job = self.pool.get_job()
            job.func()

            # execute job
            # end job
