from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests for frontend-backend communication

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["api_verse"]
apis_collection = db["apis"]

@app.route('/')
def home():
    return render_template('index.html')

# Route to add a new API
@app.route('/add_api', methods=['POST'])
def add_api():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid data"}), 400

    # Insert API data into the database
    apis_collection.insert_one(data)
    return jsonify({"message": "API added successfully"}), 201

# Route to get all APIs with descriptions included
@app.route('/get_apis', methods=['GET'])
def get_apis():
    # Fetch all APIs with uppercase DESCRIPTION field
    apis = list(apis_collection.find({}, {'_id': 0, 'name': 1, 'url': 1, 'DESCRIPTION': 1, 'category': 1}))
    # Rename the field to 'description' in the output for consistency with frontend
    for api in apis:
        api['description'] = api.pop('DESCRIPTION', 'No description available')
    return jsonify(apis), 200

@app.route('/get_apis_by_category', methods=['GET'])
def get_apis_by_category():
    category = request.args.get('category')
    if not category:
        return jsonify({"error": "Category is required"}), 400

    # Fetch APIs by category with uppercase DESCRIPTION field
    apis = list(apis_collection.find({"category": category}, {'_id': 0, 'name': 1, 'url': 1, 'DESCRIPTION': 1, 'category': 1}))
    # Rename the field to 'description' in the output for consistency with frontend
    for api in apis:
        api['description'] = api.pop('DESCRIPTION', 'No description available')
    return jsonify(apis), 200

# Route to get distinct categories from the APIs
@app.route('/get_categories', methods=['GET'])
def get_categories():
    categories = apis_collection.distinct('category')
    return jsonify(categories), 200

if __name__ == '__main__':
    app.run(debug=True)
