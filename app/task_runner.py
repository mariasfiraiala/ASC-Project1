"""Thread pool and task runner classes"""


from queue import Queue
from threading import Thread
import json
import os
from collections import OrderedDict
from app.jobs import Job

class ThreadPool:
    """Stores thread pool info"""
    def __init__(self):
        self.jobs = Queue()
        self.nr_threads = os.getenv("TP_NUM_OF_THREADS", os.cpu_count())
        self.threads = [TaskRunner(self).start() for _ in range(self.nr_threads)]
        self.status = {}

    def add_job(self, job : Job):
        """Add job to waiting queue"""
        self.status[job.id] = "running"
        self.jobs.put(job)

    def get_job(self) -> Job:
        """Get job from waiting queue"""
        return self.jobs.get()

    def get_status(self, job_id) -> dict:
        """Get status for given job id"""
        return self.status[job_id]


class TaskRunner(Thread):
    """Stores task runner info"""
    def __init__(self, pool : ThreadPool):
        super().__init__()
        self.pool = pool

    def run(self) -> None:
        """Execute jobs until done"""
        while True:
            job = self.pool.get_job()
            data = job.func(*job.args, job.data)
            self.write_data(data, job.id)
            self.pool.status[job.id] = "done"

    def write_data(self, data : dict | OrderedDict, id : int) -> None:
        """Write job result to file"""
        if not os.path.exists('results'):
            os.makedirs('results')

        with open(os.path.join("results", f"job_id{id}.json"), "w", encoding="utf-8") as fout:
            json.dump(data, fout)
