from app import webserver
from flask import request, jsonify

import os
import json
from app.jobs import *


# Example endpoint definition
@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        print(f"got data in post {data}")

        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}

        # Sending back a JSON response
        return jsonify(response)
    else:
        # Method Not Allowed
        return jsonify({"error": "Method not allowed"}), 405


@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    print(f"JobID is {job_id}")
    job_id = int(job_id)
    # Check if job_id is valid
    if job_id < 1 or job_id >= webserver.job_counter:
        return jsonify({'status': 'InvalidJobId'}), 400

    return jsonify(webserver.tasks_runner.get_status(job_id))


@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    data = request.json
    print(f"Got request {data}")

    new_job = Job(states_mean_func, webserver.job_counter, webserver.data_ingestor, data["question"])
    webserver.tasks_runner.add_job(new_job)
    webserver.job_counter += 1

    return jsonify({"job_id": new_job.id})


@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    data = request.json
    print(f"Got request {data}")

    new_job = Job(state_mean_func, webserver.job_counter, webserver.data_ingestor, data["question"], data["state"])
    webserver.tasks_runner.add_job(new_job)
    webserver.job_counter += 1

    return jsonify({"job_id": new_job.id})


@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    data = request.json
    print(f"Got request {data}")

    new_job = Job(best5_func, webserver.job_counter, webserver.data_ingestor, data["question"])
    webserver.tasks_runner.add_job(new_job)
    webserver.job_counter += 1

    return jsonify({"job_id": new_job.id})


@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    data = request.json
    print(f"Got request {data}")

    new_job = Job(worst5_func, webserver.job_counter, webserver.data_ingestor, data["question"])
    webserver.tasks_runner.add_job(new_job)
    webserver.job_counter += 1

    return jsonify({"job_id": new_job.id})


@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    data = request.json
    print(f"Got request {data}")

    new_job = Job(global_mean_func, webserver.job_counter, webserver.data_ingestor, data["question"])
    webserver.tasks_runner.add_job(new_job)
    webserver.job_counter += 1

    return jsonify({"job_id": new_job.id})


@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    data = request.json
    print(f"Got request {data}")

    new_job = Job(diff_from_mean_func, webserver.job_counter, webserver.data_ingestor, data["question"])
    webserver.tasks_runner.add_job(new_job)
    webserver.job_counter += 1

    return jsonify({"job_id": new_job.id})


@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    data = request.json
    print(f"Got request {data}")

    new_job = Job(state_diff_from_mean_func, webserver.job_counter, webserver.data_ingestor, data["question"], data["state"])
    webserver.tasks_runner.add_job(new_job)
    webserver.job_counter += 1

    return jsonify({"job_id": new_job.id})


@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    data = request.json
    print(f"Got request {data}")

    new_job = Job(mean_by_category_func, webserver.job_counter, webserver.data_ingestor, data["question"])
    webserver.tasks_runner.add_job(new_job)
    webserver.job_counter += 1

    return jsonify({"job_id": new_job.id})


@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    data = request.json
    print(f"Got request {data}")

    new_job = Job(state_mean_by_category_func, webserver.job_counter, webserver.data_ingestor, data["question"], data["state"])
    webserver.tasks_runner.add_job(new_job)
    webserver.job_counter += 1

    return jsonify({"job_id": new_job.id})


# You can check localhost in your browser to see what this displays
@webserver.route('/')
@webserver.route('/index')
def index():
    routes = get_defined_routes()
    msg = f"Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg


def get_defined_routes():
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
