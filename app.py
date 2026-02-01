from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

client = MongoClient(os.getenv("MONGO_URI"))
db = client["taskdb"]
collection = db["tasks"]

@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = []
    for task in collection.find():
        tasks.append({
            "_id": str(task["_id"]),
            "title": task["title"]
        })
    return jsonify(tasks)

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.json
    result = collection.insert_one({
        "title": data["title"]
    })
    return jsonify({"id": str(result.inserted_id)})

@app.route("/tasks/<id>", methods=["DELETE"])
def delete_task(id):
    collection.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Task deleted"})

if __name__ == "__main__":
    app.run(debug=True)
