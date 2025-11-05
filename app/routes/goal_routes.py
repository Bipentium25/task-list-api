from flask import Blueprint, abort, make_response, request, Response
from app.models.goal import Goal
from ..db import db
import os
import requests
from app.routes.route_utilities import validate_model
from ..models.task import Task

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.post("")
def create_goal():
    request_body = request.get_json()

    try: 
        new_goal = Goal.from_dict(request_body)
    except KeyError as error:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))

    db.session.add(new_goal)
    db.session.commit()

    return new_goal.to_dict(), 201

@goals_bp.get("")
def get_all_goals():
    query = db.select(Goal).order_by(Goal.id)
    goals = db.session.scalars(query)

    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())
    return goals_response


@goals_bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_goal(Goal, goal_id)
    return goal.to_dict()


@goals_bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_goal(Goal,goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    db.session.commit()


    return Response(status=204, mimetype="application/json")

@goals_bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal= validate_goal(Goal,goal_id)
    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")




def validate_goal(cls, goal_id):
    try:
        goal_id = int(goal_id)
    except:
        response = {"message": f"{cls.__name__} {goal_id} invalid"}
        abort(make_response(response , 400))

    query = db.select(cls).where(cls.id == goal_id)
    model = db.session.scalar(query)
    
    if not model:
        response = {"message": f"{cls.__name__} {goal_id} not found"}
        abort(make_response(response, 404))
    
    return model

@goals_bp.post("/<goal_id>/tasks")
def create_task_with_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    #clear
    goal.tasks.clear()

    request_body = request.get_json()
    new_tasks_ids= request_body["task_ids"]

    for new_id in new_tasks_ids:
        task = validate_model(Task,new_id)
        goal.tasks.append(task)

    db.session.commit()
    response_body = {
        "id":int(goal_id),
        "task_ids": [task.id for task in goal.tasks]
    }
    return make_response(response_body,200)


@goals_bp.get("/<goal_id>/tasks")
def get_all_task_with_goal(goal_id):

    goal = validate_model(Goal, goal_id)

    task_list = []
    for task in goal.tasks:
        each_task_info = task.to_dict()
        task_list.append(each_task_info)
    
    response = goal.to_dict()
    response["tasks"] = task_list
    return make_response(response,200)