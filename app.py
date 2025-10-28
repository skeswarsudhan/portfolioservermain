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
# uri = ""
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
# import smtplib
# from flask import Flask, request, jsonify
# from pymongo import MongoClient
# from bson.objectid import ObjectId
# from dotenv import load_dotenv
# import os
# from flask_cors import CORS
# from PIL import Image
# import io
# import base64
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

# # Load environment variables from .env file
# load_dotenv()

# app = Flask(__name__) 

# # CORS - Allow only required origins in production
# CORS(app, resources={r"/*": {"origins": ["https://portfoliofrontend-mauve.vercel.app", "http://localhost:3000", "https://skeswarsudhan.vercel.app"]}})


# # MongoDB Connection
# script_dir = os.path.dirname(os.path.abspath(__file__))
# env_path = os.path.join(script_dir, '.env')
# load_dotenv(dotenv_path=env_path, verbose=True)
# MONGO_URI = os.getenv("MONGO_URI")
# if not MONGO_URI:
#     raise ValueError("MONGO_URI is not set in the environment variables.")

# client = MongoClient(MONGO_URI)
# db = client['comments_db']

# # Collections
# comment_collection = db['comments']
# project_collection = db['projects']
# image_collection = db['images']

# def send_email_notification(name, email, comment):
#     # Load environment variables 
#     script_dir = os.path.dirname(os.path.abspath(__file__))
#     env_path = os.path.join(script_dir, '.env')
#     load_dotenv(dotenv_path=env_path, verbose=True)

#     # Retrieve email credentials
#     email_user = os.getenv("EMAIL_USER")
#     email_pass = os.getenv("EMAIL_PASS")
#     notify_email = os.getenv("NOTIFY_EMAIL")

#     # Validate email configuration
#     if not all([email_user, email_pass, notify_email]):
#         print("Email configuration is incomplete. Check your .env file.")
#         return False

#     try:
#         # Create email message
#         msg = MIMEMultipart()
#         msg['From'] = email_user
#         msg['To'] = notify_email
#         msg['Subject'] = "New Feedback Received!"

#         # Compose email body
#         body = f"""
# New feedback submitted:

# Name: {name}
# Contact Email: {email}
# Message: {comment}
# """
#         msg.attach(MIMEText(body, 'plain'))

#         # Send email via SMTP
#         with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
#             server.login(email_user, email_pass)
#             server.send_message(msg)
            
#             print("Notification email sent successfully!")
#             return True

#     except smtplib.SMTPAuthenticationError:
#         print("SMTP Authentication Error: Check your email credentials")
#         return False
#     except Exception as e:
#         print(f"Error sending email: {e}")
#         return False

# # Modify your existing add_comment route to use this function
# @app.route('/comments', methods=['POST'])
# def add_comment():
#     try:
#         data = request.get_json()
#         if not all(key in data for key in ['name', 'email', 'comment']):
#             return jsonify({'error': 'Missing required fields'}), 400

#         # Insert comment to database
#         comment_id = comment_collection.insert_one({
#             'name': data['name'],
#             'email': data['email'],
#             'comment': data['comment']
#         }).inserted_id

#         # Send email notification
#         send_email_notification(
#             name=data['name'], 
#             email=data['email'], 
#             comment=data['comment']
#         )

#         return jsonify({
#             'message': 'Comment added successfully!', 
#             'comment_id': str(comment_id)
#         }), 201

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
# # ----- Routes -----

# @app.route('/hello', methods=['GET'])
# def hello_server():
#     return "hello"
    
    
# # Add a new comment
# # @app.route('/comments', methods=['POST'])
# # def add_comment():
# #     try:
# #         data = request.get_json()
# #         if not all(key in data for key in ['name', 'email', 'comment']):
# #             return jsonify({'error': 'Missing required fields'}), 400

# #         comment_id = comment_collection.insert_one({
# #             'name': data['name'],
# #             'email': data['email'],
# #             'comment': data['comment']
# #         }).inserted_id
# #         send_email_notification(data['name'], data['email'], data['comment'])

# #         return jsonify({'message': 'Comment added successfully!', 'comment_id': str(comment_id)}), 201

# #     except Exception as e:
# #         return jsonify({'error': str(e)}), 500


# # Fetch all projects
# @app.route('/projects', methods=['GET'])
# def get_projects():
#     try:
#         projects = list(project_collection.find({}, ))
#         for project in projects:
#             project['_id'] = str(project['_id'])
#         return jsonify(projects), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


# # Add a new project
# @app.route('/projects', methods=['POST'])
# def add_project():
#     try:
#         data = request.get_json()
#         required_fields = ['title', 'description', 'category', 'start_date', 'end_date', 'tools_used', 'link']
#         if not all(field in data for field in required_fields):
#             return jsonify({'error': 'Missing required fields'}), 400

#         project_id = project_collection.insert_one({
#             'title': data['title'],
#             'description': data['description'],
#             'category': data['category'],
#             'start_date': data['start_date'],
#             'end_date': data['end_date'],
#             'tools_used': data['tools_used'],
#             'link': data['link']
#         }).inserted_id

#         return jsonify({'message': 'Project added successfully!', 'project_id': str(project_id)}), 201

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


# # Upload an image
# @app.route('/upload', methods=['POST'])
# def upload_image():
#     try:
#         if 'image' not in request.files or 'tag' not in request.form:
#             return jsonify({"error": "No image or tag provided"}), 400

#         image = request.files['image']
#         tag = request.form['tag']

#         img = Image.open(image)
#         img_byte_arr = io.BytesIO()
#         img.save(img_byte_arr, format=img.format)
#         img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

#         image_data = {'image': img_base64, 'tag': tag}
#         result = image_collection.insert_one(image_data)

#         return jsonify({"message": "Image uploaded", "id": str(result.inserted_id)}), 201

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
    


# # Fetch all images
# @app.route('/images', methods=['GET'])
# def get_images():
#     try:
#         images = image_collection.find({}, {"_id": 1, "image": 1, "tag": 1})
#         output = [{"id": str(img['_id']), "image": img['image'], "tag": img['tag']} for img in images]
#         return jsonify(output), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


# if __name__ == '__main__':
#     app.run()


import smtplib
from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os
from flask_cors import CORS
from PIL import Image
import io
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from threading import Thread
import socket

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__) 

# CORS - Allow only required origins in production
CORS(app, resources={r"/*": {"origins": ["https://portfoliofrontend-mauve.vercel.app", "http://localhost:3000", "https://skeswarsudhan.vercel.app"]}})


# MongoDB Connection
script_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(script_dir, '.env')
load_dotenv(dotenv_path=env_path, verbose=True)
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("MONGO_URI is not set in the environment variables.")

client = MongoClient(MONGO_URI)
db = client['comments_db']

# Collections
comment_collection = db['comments']
project_collection = db['projects']
image_collection = db['images']

def send_email_notification(name, email, comment):
    """
    Send email notification synchronously (to be called in background thread)
    """
    try:
        # Load environment variables 
        script_dir = os.path.dirname(os.path.abspath(__file__))
        env_path = os.path.join(script_dir, '.env')
        load_dotenv(dotenv_path=env_path, verbose=True)

        # Retrieve email credentials
        email_user = os.getenv("EMAIL_USER")
        email_pass = os.getenv("EMAIL_PASS")
        notify_email = os.getenv("NOTIFY_EMAIL")

        # Validate email configuration
        if not all([email_user, email_pass, notify_email]):
            app.logger.error("Email configuration is incomplete. Check your .env file.")
            return False

        # Create email message
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = notify_email
        msg['Subject'] = "New Feedback Received!"

        # Compose email body
        body = f"""
New feedback submitted:

Name: {name}
Contact Email: {email}
Message: {comment}
"""
        msg.attach(MIMEText(body, 'plain'))

        # Send email via SMTP with timeout
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=15) as server:
            server.login(email_user, email_pass)
            server.send_message(msg)
            
            app.logger.info("Notification email sent successfully!")
            return True

    except socket.timeout:
        app.logger.error("Email sending timed out")
        return False
    except smtplib.SMTPAuthenticationError:
        app.logger.error("SMTP Authentication Error: Check your email credentials")
        return False
    except Exception as e:
        app.logger.error(f"Error sending email: {e}")
        return False


def send_email_async(app_context, name, email, comment):
    """
    Wrapper function to send email in background thread with app context
    """
    with app_context:
        try:
            send_email_notification(name, email, comment)
        except Exception as e:
            app.logger.error(f"Async email sending failed: {e}")


# Add a new comment
@app.route('/comments', methods=['POST'])
def add_comment():
    try:
        data = request.get_json()
        if not all(key in data for key in ['name', 'email', 'comment']):
            return jsonify({'error': 'Missing required fields'}), 400

        # Insert comment to database
        comment_id = comment_collection.insert_one({
            'name': data['name'],
            'email': data['email'],
            'comment': data['comment']
        }).inserted_id

        # Send email notification asynchronously (non-blocking)
        email_thread = Thread(
            target=send_email_async,
            args=(app.app_context(), data['name'], data['email'], data['comment']),
            daemon=True
        )
        email_thread.start()

        # Return response immediately without waiting for email
        return jsonify({
            'message': 'Comment added successfully!', 
            'comment_id': str(comment_id)
        }), 201

    except Exception as e:
        app.logger.error(f"Error in add_comment: {e}")
        return jsonify({'error': str(e)}), 500


# ----- Routes -----

@app.route('/hello', methods=['GET'])
def hello_server():
    return "hello"


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
