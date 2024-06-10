from bson import ObjectId
from flask import Blueprint, jsonify, request
from common.db import db

users_blueprint = Blueprint("users", __name__)


@users_blueprint.route("/get", methods=["GET"])
def get_user():
    try:
        user_id = request.args.get("id")
        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401
        user = db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            return jsonify({"error": "Unauthorized"}), 401
        user["_id"] = str(user["_id"])
        return jsonify(user), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@users_blueprint.route("/get-all", methods=["GET"])
def get_all_users():
    try:
        user_id = request.headers.get("Authorization")
        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401
        user = db.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            return jsonify({"error": "Unauthorized"}), 401

        users = list(db.users.find({"role": "user"}))
        for user in users:
            user["_id"] = str(user["_id"])
            user["chats"] = db.chats.count_documents({"sender": user["_id"]})
        return jsonify(users), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@users_blueprint.route("/cards", methods=["GET"])
def cards():
    try:
        user_id = request.headers.get("Authorization")
        users = list(db.users.find({"role": "user"}))
        for user in users:
            user["_id"] = str(user["_id"])
            latest_chat = db.chats.find_one(
                {"sender": user["_id"], "receiver": "gpt"}, sort=[("created_at", -1)]
            )
            if not latest_chat:
                users.remove(user)
                continue
            user["time"] = latest_chat["created_at"]
            user["type"] = 4 if user_id in latest_chat["read_by"] else 1

        return jsonify(users), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
