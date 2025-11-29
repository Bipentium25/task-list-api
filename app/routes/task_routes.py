
from flask import Blueprint, request, Response
from app.models.task import Task
from ..db import db
from sqlalchemy import desc
from datetime import datetime
import os
import requests
from app.routes.route_utilities import validate_model, create_model

bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


@bp.post("")
def create_task():
    request_body = request.get_json()
    return create_model(Task, request_body)

@bp.get("")
def get_all_tasks():
    query = db.select(Task).order_by(Task.id)
    title_param = request.args.get("sort")
    if title_param:
        if title_param == "asc":
            query = db.select(Task).order_by(Task.title)
        elif title_param == "desc":
            query = db.select(Task).order_by(desc(Task.title))


    tasks = db.session.scalars(query)
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    return tasks_response

@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    return task.to_dict()

@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task,task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task,task_id)
    db.session.delete(task)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.patch("/<task_id>/mark_complete")
def mark_task(task_id):
    task = validate_model(Task,task_id)
    task.completed_at = datetime.now()
    
    db.session.commit()
    message_slack(task)
    
    return Response(status=204, mimetype="application/json")


def message_slack(task):
    slack_token = os.environ.get("SLACK_BOT_TOKEN")
    body = {'token': slack_token, 'channel': '#task-notifications', 'text':f'Someone just completed the task {task.title}'}
    headers = {'Authorization': slack_token}
    
    response = requests.post("https://slack.com/api/chat.postMessage", data=body, headers=headers)


@bp.patch("/<task_id>/mark_incomplete")
def unmark_task(task_id):
    task = validate_model(Task,task_id)
    task.completed_at = None
    
    db.session.commit()
    
    return Response(status=204, mimetype="application/json")



