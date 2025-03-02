# from flask import Flask, request, jsonify
# from pymongo import MongoClient
# from bson.objectid import ObjectId
# from dotenv import load_dotenv
# import os
# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi
# from flask_cors import CORS
# # from bson.objectid import ObjectId
# from PIL import Image
# import io
# import base64

# # Load environment variables from .env file
# load_dotenv()

# app = Flask(__name__)
# CORS(app)

# # Connect to MongoDB using the connection string from environment variables
# uri = "mongodb+srv://skeswarsudhan:kQHN0YckOjqefuT9@cluster0.j2l11nz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# # Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))

# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)

# db = client['comments_db']
# collection = db['comments']

# @app.route('/comments', methods=['POST'])
# def add_comment():
#     try:
#         data = request.get_json()
#         name = data['name']
#         email = data['email']
#         comment = data['comment']
#         print(request.data)
#         # Insert the comment into the database
#         comment_id = collection.insert_one({
#             'name': name,
#             'email': email,
#             'comment': comment
#         }).inserted_id
        
#         return jsonify({
#             'message': 'Comment added successfully!',   'end_date': end_date,
#             'tools_used': tools_used,
#             'link': link,
#         }).inserted_id
        
#         return jsonify({
#             'message': 'Project added successfully!',
#             'project_id': str(project_id)
#         }), 201
#     except Exception as e:
#         return jsonify({
#             'message': 'An error occurred!',
#             'error': str(e)
#         }), 400

# @app.route('/projects', methods=['GET'])
# def get_projects():
#     try:
#         projects = list(project_collection.find({}))
#         for project in projects:
#             project['_id'] = str(project['_id'])
        
#         return jsonify(projects), 200
#     except Exception as e:
#         return jsonify({
#             'message': 'An error occurred!',
#             'error': str(e)
#             'comment_id': str(comment_id)
#         }), 201
#     except Exception as e:
#         return jsonify({
#             'message': 'An error occurred!',
#             'error': str(e)
#         }), 400

# # Collection for projects
# project_collection = db['projects']

# @app.route('/projects', methods=['POST'])
# def add_project():
#     try:
#         data = request.get_json()
#         title = data['title']
#         description = data['description']
#         category = data['category']
#         start_date = data['start_date']
#         end_date = data['end_date']
#         tools_used = data['tools_used']
#         link=data['link']
        
#         # Insert the project into the database
#         project_id = project_collection.insert_one({
#             'title': title,
#             'description': description,
#             'category': category,
#             'start_date': start_date,
         
#         }), 400


# imagesdb=db['images']
# @app.route('/upload', methods=['POST'])
# def upload_image():
#     if 'image' not in request.files or 'tag' not in request.form:
#         return jsonify({"error": "No image or tag provided"}), 400

#     image = request.files['image']
#     tag = request.form['tag']

#     # Convert the image to a base64 string
#     img = Image.open(image)
#     img_byte_arr = io.BytesIO()
#     img.save(img_byte_arr, format=img.format)
#     img_byte_arr = img_byte_arr.getvalue()
#     img_base64 = base64.b64encode(img_byte_arr).decode('utf-8')

#     image_data = {
#         'image': img_base64,
#         'tag': tag
#     }

#     result = imagesdb.insert_one(image_data)
#     return jsonify({"message": "Image uploaded", "id": str(result.inserted_id)}), 201

# @app.route('/images', methods=['GET'])
# def get_images():
#     images = imagesdb.find()
#     output = []
#     for image_data in images:
#         output.append({
#             'id': str(image_data['_id']),
#             'image': image_data['image'],
#             'tag': image_data['tag']
#         })
#     return jsonify(output)


# if __name__ == '__main__':
#     app.run()

from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os
from flask_cors import CORS
from PIL import Image
import io
import base64

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# CORS - Allow only required origins in production
CORS(app, resources={r"/*": {"origins": "*"}})

# MongoDB Connection
MONGO_URI = "mongodb+srv://skeswarsudhan:kQHN0YckOjqefuT9@cluster0.j2l11nz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
if not MONGO_URI:
    raise ValueError("MONGO_URI is not set in the environment variables.")

client = MongoClient(MONGO_URI)
db = client['comments_db']

# Collections
comment_collection = db['comments']
project_collection = db['projects']
image_collection = db['images']

# ----- Routes -----

@app.route('/hello', methods=['GET'])
def hello_server():
    return "hello"
    
    
# Add a new comment
@app.route('/comments', methods=['POST'])
def add_comment():
    try:
        data = request.get_json()
        if not all(key in data for key in ['name', 'email', 'comment']):
            return jsonify({'error': 'Missing required fields'}), 400

        comment_id = comment_collection.insert_one({
            'name': data['name'],
            'email': data['email'],
            'comment': data['comment']
        }).inserted_id

        return jsonify({'message': 'Comment added successfully!', 'comment_id': str(comment_id)}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Fetch all projects
@app.route('/projects', methods=['GET'])
def get_projects():
    try:
        projects = list(project_collection.find({}, ))
        for project in projects:
            project['_id'] = str(project['_id'])
        return jsonify(projects), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Add a new project
@app.route('/projects', methods=['POST'])
def add_project():
    try:
        data = request.get_json()
        required_fields = ['title', 'description', 'category', 'start_date', 'end_date', 'tools_used', 'link']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        project_id = project_collection.insert_one({
            'title': data['title'],
            'description': data['description'],
            'category': data['category'],
            'start_date': data['start_date'],
            'end_date': data['end_date'],
            'tools_used': data['tools_used'],
            'link': data['link']
        }).inserted_id

        return jsonify({'message': 'Project added successfully!', 'project_id': str(project_id)}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Upload an image
@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        if 'image' not in request.files or 'tag' not in request.form:
            return jsonify({"error": "No image or tag provided"}), 400

        image = request.files['image']
        tag = request.form['tag']

        img = Image.open(image)
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format=img.format)
        img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

        image_data = {'image': img_base64, 'tag': tag}
        result = image_collection.insert_one(image_data)

        return jsonify({"message": "Image uploaded", "id": str(result.inserted_id)}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    


# Fetch all images
@app.route('/images', methods=['GET'])
def get_images():
    try:
        images = image_collection.find({}, {"_id": 1, "image": 1, "tag": 1})
        output = [{"id": str(img['_id']), "image": img['image'], "tag": img['tag']} for img in images]
        return jsonify(output), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run()
