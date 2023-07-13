from flask import Flask,jsonify, request
from pymongo import MongoClient
import json
from bson import ObjectId

app = Flask(__name__)

# MongoDB connection details
client = MongoClient('mongodb://localhost:27017/')
db = client['myDatabase']
collection = db['mycollection']

@app.route('/create', methods=['POST'])
def create():
    # data = {
    #         'name':"john",
    #         "age":25
    # }
    data = request.get_json()
    result = collection.insert_one(data)
    return jsonify({
        'message': 'Data created successfully',
        'inserted_id': str(result.inserted_id)
    })

#reading data
@app.route('/read', methods=['GET'])
def read():
    data = list(collection.find())
    # Convert ObjectId to string
    for doc in data:
        doc['_id'] = str(doc['_id']) # here I am converting the type of Id into string
    return jsonify(data)


@app.route('/update/<id>', methods=['PUT'])
def update(id):
    query = {'_id': ObjectId(id)}
    updated_data = request.get_json()
    # updated_data['_id'] = ObjectId(id)  # Include the ID in the updated data
    collection.replace_one(query, updated_data)
    return jsonify({'message': 'Data updated successfully'})

@app.route('/delete/<id>', methods = ['DELETE'])
def delete(id):
    query = {'_id': ObjectId(id)}
    collection.delete_one(query)
    return jsonify({'message': 'Data deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)