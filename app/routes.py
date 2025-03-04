"""Routes for flask server"""


import os
import json
import logging
from flask import request, jsonify
from app import webserver
from app.jobs import Job, states_mean_func, state_mean_func, best5_func
from app.jobs import worst5_func, global_mean_func, diff_from_mean_func
from app.jobs import state_diff_from_mean_func, mean_by_category_func, state_mean_by_category_func


@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    """Gets result of given job id"""

    job_id = int(job_id)
    logging.info("Got request for job id %d", job_id)

    if job_id < 1 or job_id >= webserver.job_counter:
        return jsonify({"status": "InvalidJobId"}), 400

    if webserver.tasks_runner.get_status(job_id) == "running":
        return jsonify({"status": "running"})

    with open(os.path.join("results", f"job_id{job_id}.json"), "r", encoding="utf-8") as fin:
        data = json.load(fin)

    return jsonify({"status": "done", "data": data})


@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    """Register states mean job"""

    data = request.json
    logging.info("Got request for job %s with input: %s", request.path, data)

    new_job = Job(states_mean_func, webserver.job_counter, webserver.data_ingestor,
                  data["question"])
    webserver.tasks_runner.add_job(new_job)

    with webserver.id_lock:
        webserver.job_counter += 1

    return jsonify({"job_id": new_job.id})


@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    """Register state mean job"""

    data = request.json
    logging.info("Got request for job %s with input: %s", request.path, data)

    new_job = Job(state_mean_func, webserver.job_counter, webserver.data_ingestor,
                  data["question"], data["state"])
    webserver.tasks_runner.add_job(new_job)

    with webserver.id_lock:
        webserver.job_counter += 1

    return jsonify({"job_id": new_job.id})


@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    """Register best5 job"""

    data = request.json
    logging.info("Got request for job %s with input: %s", request.path, data)

    new_job = Job(best5_func, webserver.job_counter, webserver.data_ingestor,
                  data["question"])
    webserver.tasks_runner.add_job(new_job)

    with webserver.id_lock:
        webserver.job_counter += 1

    return jsonify({"job_id": new_job.id})


@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    """Register worst5 job"""

    data = request.json
    logging.info("Got request for job %s with input: %s", request.path, data)

    new_job = Job(worst5_func, webserver.job_counter, webserver.data_ingestor,
                  data["question"])
    webserver.tasks_runner.add_job(new_job)

    with webserver.id_lock:
        webserver.job_counter += 1

    return jsonify({"job_id": new_job.id})


@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    """Register global mean job"""

    data = request.json
    logging.info("Got request for job %s with input: %s", request.path, data)

    new_job = Job(global_mean_func, webserver.job_counter, webserver.data_ingestor,
                  data["question"])
    webserver.tasks_runner.add_job(new_job)

    with webserver.id_lock:
        webserver.job_counter += 1

    return jsonify({"job_id": new_job.id})


@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    """Register diff from mean job"""

    data = request.json
    logging.info("Got request for job %s with input: %s", request.path, data)

    new_job = Job(diff_from_mean_func, webserver.job_counter, webserver.data_ingestor,
                  data["question"])
    webserver.tasks_runner.add_job(new_job)

    with webserver.id_lock:
        webserver.job_counter += 1

    return jsonify({"job_id": new_job.id})


@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    """Register state diff from mean job"""

    data = request.json
    logging.info("Got request for job %s with input: %s", request.path, data)

    new_job = Job(state_diff_from_mean_func, webserver.job_counter, webserver.data_ingestor,
                  data["question"], data["state"])
    webserver.tasks_runner.add_job(new_job)

    with webserver.id_lock:
        webserver.job_counter += 1

    return jsonify({"job_id": new_job.id})


@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    """Register mean by category job"""

    data = request.json
    logging.info("Got request for job %s with input: %s", request.path, data)

    new_job = Job(mean_by_category_func, webserver.job_counter, webserver.data_ingestor,
                  data["question"])
    webserver.tasks_runner.add_job(new_job)

    with webserver.id_lock:
        webserver.job_counter += 1

    return jsonify({"job_id": new_job.id})


@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    """Register state mean by category job"""

    data = request.json
    logging.info("Got request for job %s with input: %s", request.path, data)

    new_job = Job(state_mean_by_category_func, webserver.job_counter, webserver.data_ingestor,
                  data["question"], data["state"])
    webserver.tasks_runner.add_job(new_job)

    with webserver.id_lock:
        webserver.job_counter += 1

    return jsonify({"job_id": new_job.id})


@webserver.route('/api/graceful_shutdown', methods=['GET'])
def graceful_shutdown_request():
    """Register graceful shutdown job"""

    logging.info("Got request to shut down")
    webserver.tasks_runner.shutdown()
    logging.info("Shutting down...")
    return jsonify({"shutdown": "True"})


@webserver.route('/api/jobs', methods=['GET'])
def jobs_request():
    """Register jobs job"""

    logging.info("Got request to print all jobs")
    return jsonify({"status": "done",
                    "data": webserver.tasks_runner.get_status_all(webserver.job_counter)})


@webserver.route('/api/num_jobs', methods=['GET'])
def num_jobs_request():
    """Register num jobs job"""

    logging.info("Got request to print all pending jobs")
    return jsonify(webserver.tasks_runner.get_remaining_jobs())


# You can check localhost in your browser to see what this displays
@webserver.route('/')
@webserver.route('/index')
def index():
    """Get server usage"""

    routes = get_defined_routes()
    msg = f"Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg


def get_defined_routes():
    """Get all server routes"""

    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
