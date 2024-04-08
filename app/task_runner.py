from queue import Queue
from threading import Thread, Event
import time
import os
from app.jobs import Job

class ThreadPool:
    def __init__(self):
        self.jobs = Queue()
        self.nr_threads = os.getenv("TP_NUM_OF_THREADS", os.cpu_count())
        self.threads = [TaskRunner(self).start() for _ in range(self.nr_threads)]
        self.status = {}

    def add_job(self, job : Job):
        self.status[job.id] = {"status": "running"}
        self.jobs.put(job)

    def get_job(self) -> Job:
        return self.jobs.get()

    def get_status(self, job_id) -> dict:
        return self.status[job_id]


class TaskRunner(Thread):
    def __init__(self, pool : ThreadPool):
        super().__init__()
        self.pool = pool

    def run(self) -> None:
        while True:
            job = self.pool.get_job()
            res = job.func(*job.args, job.data)
            self.pool.status[job.id] = {"status": "done", "data": res}

