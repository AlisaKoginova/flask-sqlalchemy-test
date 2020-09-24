from flask import request

def get_request_data():
    """
    Get keys & values from request
    """
    if request.is_json:
        data = request.json
    else:
        data = request.form.to_dict()
    return data
