"""Setup for basic master - workers server"""

import logging
import logging.handlers
import time
from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool
from threading import Lock

werkzeug_logger = logging.getLogger("werkzeug")
werkzeug_logger.setLevel(logging.ERROR)

webserver = Flask(__name__)
webserver.tasks_runner = ThreadPool()
webserver.json.sort_keys = False

logging.basicConfig(level=logging.INFO, filename="webserver.log")

logger = logging.getLogger(None)
handler = logging.handlers.RotatingFileHandler("webserver.log", maxBytes=100000, backupCount=20)
formatter = logging.Formatter("%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s")
formatter.converter = time.gmtime
handler.setFormatter(formatter)
logger.addHandler(handler)

webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")
webserver.job_counter = 1
webserver.id_lock = Lock()

from app import routes
