from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Connect to MongoDB using the connection string from environment variables
# mongo_uri = 'mongodb+srv://skeswarsudhan:kQHN0YckOjqefuT9@cluster0.j2l11nz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
# client = MongoClient(mongo_uri)



uri = "mongodb+srv://skeswarsudhan:kQHN0YckOjqefuT9@cluster0.j2l11nz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
db = client['comments_db']
collection = db['comments']
@app.route('/comments', methods=['POST'])
def add_comment():
    try:
        data = request.get_json()
        name = data['name']
        email = data['email']
        comment = data['comment']
        
        # Insert the comment into the database
        comment_id = collection.insert_one({
            'name': name,
            'email': email,
            'comment': comment
        }).inserted_id
        
        return jsonify({
            'message': 'Comment added successfully!',
            'comment_id': str(comment_id)
        }), 201
    except Exception as e:
        return jsonify({
            'message': 'An error occurred!',
            'error': str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True)
