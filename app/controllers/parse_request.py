from flask import request


def get_request_data():
    """
    Get keys & values from request
    """
    data = dict(request.form)
    return data
