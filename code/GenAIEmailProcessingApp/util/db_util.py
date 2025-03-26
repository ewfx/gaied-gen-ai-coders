from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class RequestType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_type = db.Column(db.String(80), nullable=False)
    sub_request_type = db.Column(db.String(200), nullable=True)  # This line remains unchanged

# Cache for request types
request_types_cache = None

def initialize_db():
    db.create_all()

from .db_util import db, RequestType, request_types_cache

def load_request_types_from_db():
    global request_types_cache
    if request_types_cache is not None:
        print("Loading request types from cache.")
        return request_types_cache

    print("Loading request types from database using SQLAlchemy.")
    request_types = RequestType.query.all()
    result = {}
    for request_type in request_types:
        if request_type.request_type not in result:
            result[request_type.request_type] = {
                "requestType": request_type.request_type,
                "subRequestTypes": []
            }
        if request_type.sub_request_type:
            result[request_type.request_type]["subRequestTypes"].append(request_type.sub_request_type)
    print("Loaded request types from database.")
    request_types_cache = list(result.values())
    return request_types_cache

def clear_request_types_cache():
    global request_types_cache
    request_types_cache = None
