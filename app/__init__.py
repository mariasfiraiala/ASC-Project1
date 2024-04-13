from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool
from threading import Lock


webserver = Flask(__name__)
webserver.tasks_runner = ThreadPool()
webserver.json.sort_keys = False

webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")
webserver.job_counter = 1
webserver.id_lock = Lock()

from app import routes
