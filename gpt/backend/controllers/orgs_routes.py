from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from pymongo import MongoClient
from common.db import db

organizations_collection = db['organizations']

orgs_blueprint = Blueprint('orgs_blueprint', __name__)

# Create a new organization
@orgs_blueprint.route('/', methods=['POST'])
def add_organization():
    data = request.get_json()
    result = organizations_collection.insert_one(data)
    return jsonify(str(result.inserted_id)), 201

# Get all organizations
@orgs_blueprint.route('/', methods=['GET'])
def get_organizations():
    print(1)
    organizations = list(organizations_collection.find())
    for organization in organizations:
        organization['_id'] = str(organization['_id'])
    return jsonify(organizations), 200

# Get a specific organization
@orgs_blueprint.route('/<id>', methods=['GET'])
def get_organization(id):
    organization = organizations_collection.find_one({'_id': ObjectId(id)})
    if organization:
        organization['_id'] = str(organization['_id'])
        return jsonify(organization), 200
    else:
        return jsonify({'error': 'Organization not found'}), 404

# Update an organization
@orgs_blueprint.route('/<id>', methods=['PUT'])
def update_organization(id):
    data = request.get_json()
    result = organizations_collection.update_one({'_id': ObjectId(id)}, {'$set': data})
    if result.matched_count:
        return jsonify({'msg': 'Organization updated'}), 200
    else:
        return jsonify({'error': 'Organization not found'}), 404

# Delete an organization
@orgs_blueprint.route('/<id>', methods=['DELETE'])
def delete_organization(id):
    result = organizations_collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count:
        return jsonify({'msg': 'Organization deleted'}), 200
    else:
        return jsonify({'error': 'Organization not found'}), 404
