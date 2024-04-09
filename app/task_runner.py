from queue import Queue
from threading import Thread, Event
import json
import os
from app.jobs import Job
from collections import OrderedDict

class ThreadPool:
    def __init__(self):
        self.jobs = Queue()
        self.nr_threads = os.getenv("TP_NUM_OF_THREADS", os.cpu_count())
        self.threads = [TaskRunner(self).start() for _ in range(self.nr_threads)]
        self.status = {}

    def add_job(self, job : Job):
        self.status[job.id] = "running"
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
            data = job.func(*job.args, job.data)
            self.write_data(data, job.id)
            self.pool.status[job.id] = "done"


    def write_data(self, data : dict | OrderedDict, id : int) -> None:
        if not os.path.exists('results'):
            os.makedirs('results')

        with open(os.path.join("results", f"job_id{id}.json"), "w") as fout:
            json.dump(data, fout)
