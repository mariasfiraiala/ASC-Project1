"""Thread pool and task runner classes"""


from operator import countOf
from queue import Queue
from threading import Thread, Event
import json
import os
from collections import OrderedDict
from app.jobs import Job

class ThreadPool:
    """Stores thread pool info"""
    def __init__(self):
        self.jobs = Queue()
        self.done = Event()
        self.status = {}
        self.nr_threads = os.getenv("TP_NUM_OF_THREADS", os.cpu_count())
        self.threads = [TaskRunner(self) for _ in range(self.nr_threads)]

        for t in self.threads:
            t.start()

    def add_job(self, job : Job):
        """Add job to waiting queue"""
        if not self.done.is_set():
            self.status[job.id] = "running"
            self.jobs.put(job)

    def get_job(self) -> Job:
        """Get job from waiting queue"""
        return self.jobs.get(timeout=0.5)

    def get_status(self, job_id) -> dict:
        """Get status for given job id"""
        return self.status[job_id]

    def get_status_all(self, current_job_id : int) -> dict:
        """Get status for all jobs up until current unused id"""
        return [{f'job_id_{i}': self.status[i]} for i in range(1, current_job_id)]

    def get_remaining_jobs(self) -> dict:
        """Get waiting and running jobs"""
        return {"num_jobs": countOf(self.status.values(), "running")}

    def shutdown(self) -> None:
        """Signal all threads to stop"""
        self.done.set()

        for t in self.threads:
            t.join()


class TaskRunner(Thread):
    """Stores task runner info"""
    def __init__(self, pool : ThreadPool):
        super().__init__()
        self.pool = pool

    def run(self) -> None:
        """Execute jobs until done"""
        while not self.pool.done.is_set() or not self.pool.jobs.empty():
            try:
                job = self.pool.get_job()
                data = job.func(*job.args, job.data)
                self.write_data(data, job.id)
                self.pool.status[job.id] = "done"
            except:
                pass

    def write_data(self, data : dict | OrderedDict, id : int) -> None:
        """Write job result to file"""
        if not os.path.exists('results'):
            os.makedirs('results')

        with open(os.path.join("results", f"job_id{id}.json"), "w", encoding="utf-8") as fout:
            json.dump(data, fout)
