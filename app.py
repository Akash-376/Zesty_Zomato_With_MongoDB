from flask import Flask, request, jsonify
from flask_cors import CORS # to handle CORS policy error
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# my_data = []

# my_orders = []

# MongoDB connection details
client = MongoClient('mongodb://localhost:27017/')
db = client['zesty_zomato']

dishes = db['dishes']   # this is collection
orders = db['orders']   # this is collection


# add new Dish
@app.route('/dishes', methods=['POST'])
def add_item():

    new_dish = request.get_json()
    result = dishes.insert_one(new_dish)
    return jsonify({
        'message': 'Dish added successfully',
        'inserted_id': str(result.inserted_id)
    })

# get all dishes
@app.route('/')
def get_all_dishes():

    data = list(dishes.find())
    if len(data) == 0:
        return jsonify([{'success': False,'message' : 'No any Dish available yet!'}])
    else:
        for doc in data:
            doc['_id'] = str(doc['_id']) # here I am converting the type of Id into string
        return jsonify(data)
    

# get specific dish by dish_id
@app.route('/dishes/<dish_id>')
def get_dish(dish_id):
    query = {'_id': ObjectId(dish_id)}
    dish = dishes.find_one(query)

    # if dish is found
    if dish:
        dish['_id'] = str(dish['_id'])
        return jsonify(dish)

    return jsonify({'success': False,'message': 'dish not found with this Id'})



# update specific dish by dish_id
@app.route('/dishes/<dish_id>', methods=['PUT'])
def update_dish(dish_id):

    query = {'_id': ObjectId(dish_id)}
    dish = dishes.find_one(query)
    
    # if dish is found
    if dish:
        updated_dish = request.get_json()
        # updated_dish['_id'] = ObjectId(dish_id)
        dishes.replace_one(query, updated_dish)
        return jsonify({'message': 'dish updated successfully'})

    return jsonify({'success': False,'message': 'dish not found with this Id'})





# http://127.0.0.1:5000/dishes/1?availability=False/True
# update availability status of a specific dish by dish_id
# @app.route('/dishes/<dish_id>', methods=['PUT'])
# def update_dish_availability(dish_id):
#     query = {'_id': ObjectId(dish_id)}
#     updated_data = {'$set': {'availability': request.args.get('availability')}}
#     update_result = dishes.update_one(query, updated_data)

#     if update_result.modified_count > 0:
#         return jsonify({'message': 'Dish availability status updated successfully'})
#     else:
#         return jsonify({'success': False, 'message': 'Dish not found with this ID'})



# Delete dish by Id
@app.route('/dishes/<dish_id>', methods=['DELETE'])
def remove_dish(dish_id):

    query = {'_id': ObjectId(dish_id)}
    dish = dishes.find_one(query)
    if dish:
        dishes.delete_one(query)
        return jsonify({'message': 'dish deleted successfully'})
    
    return jsonify({'success': False, 'message': 'Dish not found in the menu!'})


# function to take order from customers
@app.route('/orders/<dish_id>', methods = ['POST'])
def place_order(dish_id):

    query = {"_id": ObjectId(dish_id)}
    dish = dishes.find_one(query)

    if dish:
        
        if  dish["availability"] == "true":
            order = {**dish}
            order['customer_name'] = request.json['customer_name']
            order['order_status'] = 'Pending'
            result = orders.insert_one(order)
            return jsonify({
                'message': 'Order placed Successfully',
                'inserted_id': str(result.inserted_id)
            })
        return jsonify({'success': False,'message' : 'Sorry! this Dish is Currently Unavailable'})

    return jsonify({'success': False, 'message': 'Dish not found in the menu!'})




# get all orders
@app.route('/orders')
def get_all_orders():
    data = list(orders.find())
    if len(data) == 0:
        return jsonify([{'success': False,'message' : 'Not any order found'}])
    for doc in data:
        doc["_id"] = str(doc["_id"])
    return jsonify(data)


# get specific order by order_id
@app.route('/orders/<order_id>')
def get_order(order_id):
    query = {"_id": ObjectId(order_id)}
    order = orders.find_one(query)
    if order:
        order["_id"] = str(order["_id"])
        return jsonify(order)
    return {'success': False,'message': 'order not found with this Id'}

# http://127.0.0.1:5000/orders/1?order_status=delivered
# update order status of a specific dish by dish_id
@app.route('/orders/<order_id>', methods=['PUT'])
def update_order_status(order_id):

    query = {"_id": ObjectId(order_id)}
    order = orders.find_one(query)
    if order:
        order["_id"] = str(order["_id"])
        new_status =  request.args.get('order_status')
        orders.update_one(query, {'$set': {'order_status': new_status}})
        return jsonify(order)
    return {'success': False,'message': 'order not found with this Id'}




if __name__ == '__main__':
    app.run()