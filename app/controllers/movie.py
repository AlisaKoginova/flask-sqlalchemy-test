from flask import jsonify, make_response
from ast import literal_eval
from datetime import datetime as dt

from models.movie import Movie
from models.actor import Actor
from settings.constants import MOVIE_FIELDS
from .parse_request import get_request_data

def get_all_movies():
    all_movies = Movie.query.all()
    movies = []
    for mov in all_movies:
        act = {k: v for k, v in mov.__dict__.items() if k in MOVIE_FIELDS}
        movies.append(act)
    return make_response(jsonify(movies), 200)


def get_movie_by_id():
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

        obj = Movie.query.filter_by(id=row_id).first()
        try:
            movie = {k: v for k, v in obj.__dict__.items() if k in MOVIE_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)

        return make_response(jsonify(movie), 200)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)


def add_movie():
    """
    Add new movie
    """

    data = get_request_data()
    try:
        if data['year'].isdigit() and len(data['year']) == 4 and data['genre'].isalpha():
            new_record = Movie.create(**data)
            new_movie = {k: v for k, v in new_record.__dict__.items() if k in MOVIE_FIELDS}
            return make_response(jsonify(new_movie), 200)
        else:
            return make_response(jsonify(error='ERROR'), 400)

    except:
        return make_response(jsonify(error='ERROR'), 400)


def update_movie():
    """
    Update movie record by id
    """
    data = get_request_data()
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
            if data['year'].isdigit() and len(data['year']) == 4 and data['genre'].isalpha():
                upd_record = Movie.update(row_id, **data)
                upd_movie = {k: v for k, v in upd_record.__dict__.items() if k in MOVIE_FIELDS}
                return make_response(jsonify(upd_movie), 200)
            else:
                return make_response(jsonify(error='ERROR'), 400)

        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)


def delete_movie():
    """
    Delete movie by id
    """
    data = get_request_data()
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
            Movie.delete(row_id)
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)

    msg = 'Record successfully deleted'
    return make_response(jsonify(message=msg), 200)


def movie_add_relation():
    """
    Add actor to movie's cast
    """
    data = get_request_data()
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
            relation_id = data['relation_id']
            obj_actor = Actor.query.filter_by(id=relation_id).first()
            movie = Movie.add_relation(row_id, obj_actor)
            rel_movie = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
            rel_movie['cast'] = str(movie.cast)
            return make_response(jsonify(rel_movie), 200)

        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)

def movie_clear_relations():
    """
    Clear all relations by id
    """
    data = get_request_data()
    if 'id' in data.keys():
        try:
            movie_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
        movie = Movie.clear_relations(movie_id)
        try:
            rel_movie = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)
        rel_movie['cast'] = str(movie.cast)
        return make_response(jsonify(rel_movie), 200)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)
