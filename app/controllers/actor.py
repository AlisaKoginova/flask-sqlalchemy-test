from flask import jsonify, make_response

from app.models.actor import Actor
from app.models.movie import Movie
from ..settings.constants import ACTOR_FIELDS
from .parse_request import get_request_data


def get_all_actors():
    """
    Get list of all records
    """
    all_actors = Actor.query.all()
    actors = []
    for actor in all_actors:
        act = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
        actors.append(act)
    return make_response(jsonify(actors), 200)


def get_actor_by_id():
    """
    Get record by id
    """
    data = get_request_data()
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)

        obj = Actor.query.filter_by(id=row_id).first()
        try:
            actor = {k: v for k, v in obj.__dict__.items() if k in ACTOR_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)

        return make_response(jsonify(actor), 200)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)


def add_actor():
    """
    Add new actor
    """
    data = get_request_data()

    new_record = Actor.create(**data)
    new_actor = {k: v for k, v in new_record.__dict__.items() if k in ACTOR_FIELDS}
    return make_response(jsonify(new_actor), 200)


def update_actor():
    """
    Update actor record by id
    """
    data = get_request_data()
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)

    upd_record = Actor.update(row_id, **data)
    upd_actor = {k: v for k, v in upd_record.__dict__.items() if k in ACTOR_FIELDS}
    return make_response(jsonify(upd_actor), 200)


def delete_actor():
    """
    Delete actor by id
    """
    data = get_request_data()
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
            Actor.delete(row_id)
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)

    msg = 'Record successfully deleted'
    return make_response(jsonify(message=msg), 200)


def actor_add_relation():
    """
    Add a movie to actor's filmography
    """
    data = get_request_data()
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
            relation_id = data['relation_id']
            obj_movie = Movie.query.filter_by(id=relation_id).first()
            actor = Actor.add_relation(row_id, obj_movie)
            rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
            rel_actor['filmography'] = str(actor.filmography)
            return make_response(jsonify(rel_actor), 200)

        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)


def actor_clear_relations():
    """
    Clear all relations by id
    """
    data = get_request_data()
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
            actor = Actor.clear_relations(row_id)
            rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
            rel_actor['filmography'] = str(actor.filmography)
            return make_response(jsonify(rel_actor), 200)
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)


