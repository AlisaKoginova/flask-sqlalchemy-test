from flask import Flask, request
from flask import current_app as app

from controllers.actor import *
from controllers.movie import *

@app.route('/api/actors', methods=['GET'])
def actors():
    return get_all_actors()

@app.route('/api/actor', methods=['GET', 'POST', 'PUT', 'DELETE'])
def actor():
    if request.method == 'GET':
        return get_actor_by_id()
    if request.method == 'POST':
        return add_actor()
    if request.method == 'PUT':
        return update_actor()
    if request.method == 'DELETE':
        return delete_actor()

@app.route('/api/actor-relations', methods=['PUT', 'DELETE'])
def actor_relations():
    if request.method == 'PUT':
        return actor_add_relation()
    elif request.method == 'DELETE':
        return actor_clear_relations()

@app.route('/api/movies', methods=['GET'])
def movies():
    return get_all_movies()

@app.route('/api/movie', methods=['GET', 'POST', 'PUT', 'DELETE'])
def movie():
    if request.method == 'GET':
        return get_movie_by_id()
    if request.method == 'POST':
        return add_movie()
    if request.method == 'PUT':
        return update_movie()
    if request.method == 'DELETE':
        return delete_movie()

@app.route('/api/movie-relations', methods=['PUT', 'DELETE'])
def movie_relations():
    if request.method == 'PUT':
        return movie_add_relation()
    if request.method == 'DELETE':
        return movie_clear_relations()
