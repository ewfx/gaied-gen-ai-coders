import os
from apiflask import APIFlask, Schema
from flask import Flask, render_template, request, jsonify, current_app
from util.email_classification import summarize_eml_file
from flask_bootstrap import Bootstrap5
import json
from util.db_util import db, RequestType, initialize_db, clear_request_types_cache  # Import clear_request_types_cache
from apiflask.fields import File, Float, List, Nested, Dict, String, Integer  # Import necessary fields

app = APIFlask(__name__, title='GenAI Email Processing API', version='1.0', static_folder='static')

app.servers = [
    {
        "url": "http://localhost:5000",
        "name": "Local server"
    },
    {
        "url": "https://genai-email-processing-app-450383511585.asia-south1.run.app/",
        "name": "Sandbox server"
    }
]
# Define the upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("EMAIL_PROC_APP_DB") or os.getenv("EMAIL_PROC_APP_DB")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)  # Initialize the database with the app

# Create the upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

Bootstrap5(app)

with app.app_context():
    initialize_db()  # Create tables if they don't exist


class Email(Schema):
    files = File(required=True)  # Ensure the file field is required

class RequestClassification(Schema):
    confidenceScore = Float()
    requestType = String()
    sub_requestTypes = List(String())

class RequestTypeClassification(Schema):
    id = Integer()
    request_type = String()
    sub_request_type = String()

class RequestTypeClassificationWithoutId(Schema):
    request_type = String()
    sub_request_type = String()
    

class Result(Schema):
    keyFields = Dict()
    message = String()
    requestClassification = List(Nested(RequestClassification))
    summary = String()

class ProcessEmailResponse(Schema):
    message = String()
    file_name = String()
    results = List(Nested(Result))

@app.route("/")
@app.doc(hide=True)
def index():
    return render_template("index.html")

@app.route("/process_email_page")
@app.doc(hide=True)
def process_email_page():
    return render_template("process_email.html")

@app.route("/request_types_page")
@app.doc(hide=True)
def request_types_page():
    return render_template("request_types.html")

@app.route("/process_email", methods=["POST"])
@app.input(Email, location='files')
@app.output(ProcessEmailResponse)  # Add output schema
def process_email(files_data):
    if request.method == "POST":
        print('Request files:', request.files)  # Debugging statement
        print('Request form:', request.form)    # Debugging statement
        print('Request data:', request.data)    # Debugging statement
        print('files_data:', files_data)        # Debugging statement
        
        if not files_data:
            return jsonify({
                "message": "No file uploaded",
                "file_name": None,
                "results": None
            }), 400
        
        file = files_data.get("files")
        print('File:', file)  # Debugging statement
        # Process the file and parameters here
        if file:
            # Get the filename
            filename = file.filename
            # Construct the full filepath
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            # Save the file
            file.save(filepath)
        
            summary = summarize_eml_file(filepath)
            summary = summary.replace("```json", "").replace("```", "")  # Remove JSON formatting
            print('Summary:', summary)  # Debugging statement
        else:
            summary = None
        
        response = {
            "message": "File uploaded and parameters received",
            "file_name": file.filename if file else None,
            "results": json.loads(summary) if summary else None  # Convert summary to JSON object if not None
        }
        return jsonify(response)
    return render_template("upload.html")

@app.route("/request_types", methods=["GET"])
@app.output(RequestTypeClassification(many=True))
def get_request_types():
    request_types = RequestType.query.all()
    return jsonify([{
        "id": rt.id,
        "request_type": rt.request_type,
        "sub_request_type": rt.sub_request_type
    } for rt in request_types])

@app.route("/request_types", methods=["POST"])
@app.input(RequestTypeClassificationWithoutId, location='json')
@app.output(RequestTypeClassification)
def create_request_type(json_data):
    new_request_type = RequestType(
        request_type=json_data.get("request_type"),
        sub_request_type=json_data.get("sub_request_type")
    )
    db.session.add(new_request_type)
    db.session.commit()
    clear_request_types_cache()  # Clear cache on data update
    return jsonify({
        "id": new_request_type.id,
        "request_type": new_request_type.request_type,
        "sub_request_type": new_request_type.sub_request_type
    }), 201

@app.route("/request_types/<int:id>", methods=["GET"])
@app.output(RequestTypeClassification)
def get_request_type(id):
    request_type = RequestType.query.get_or_404(id)
    return jsonify({
        "id": request_type.id,
        "request_type": request_type.request_type,
        "sub_request_type": request_type.sub_request_type
    })

@app.route("/request_types/<int:id>", methods=["PUT"])
@app.input(RequestTypeClassificationWithoutId, location='json')
@app.output(RequestTypeClassification)
def update_request_type(id, json_data):
    request_type = RequestType.query.get_or_404(id)
    request_type.request_type = json_data.get("request_type", request_type.request_type)
    request_type.sub_request_type = json_data.get("sub_request_type", request_type.sub_request_type)
    db.session.commit()
    clear_request_types_cache()  # Clear cache on data update
    return jsonify({
        "id": request_type.id,
        "request_type": request_type.request_type,
        "sub_request_type": request_type.sub_request_type
    })

@app.route("/request_types/<int:id>", methods=["DELETE"])
def delete_request_type(id):
    request_type = RequestType.query.get_or_404(id)
    db.session.delete(request_type)
    db.session.commit()
    clear_request_types_cache()  # Clear cache on data update
    return '', 204

@app.route("/load_request_types", methods=["POST"])
@app.doc(hide=True)
@app.output({"message": String()})  # Remove methods argument
def load_request_types():
    with current_app.open_resource('input/requestTypes.json') as f:
        data = json.load(f)
        for item in data['requestTypes']:
            request_type = item['requestType']
            sub_request_types = item.get('subRequestTypes', [])
            if not sub_request_types:
                existing = RequestType.query.filter_by(request_type=request_type, sub_request_type=None).first()
                if not existing:
                    new_request_type = RequestType(
                        request_type=request_type,
                        sub_request_type=None
                    )
                    db.session.add(new_request_type)
            for sub_request_type in sub_request_types:
                existing = RequestType.query.filter_by(request_type=request_type, sub_request_type=sub_request_type).first()
                if not existing:
                    new_request_type = RequestType(
                        request_type=request_type,
                        sub_request_type=sub_request_type
                    )
                    db.session.add(new_request_type)
        db.session.commit()
        clear_request_types_cache()  # Clear cache on data update
    return jsonify({"message": "Request types loaded successfully"}), 201


