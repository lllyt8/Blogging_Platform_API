import os
from flask import Flask, request, jsonify, abort
from datetime import datetime

app = Flask(__name__)


posts = []
next_id = 1


def get_current_time():
    return datetime.utcnow().isoformat() + "Z"

# Data Validation
def validate_post_data(data):
    required_fields = ["title", "content", "category", "tags"]
    errors = {}
    for field in required_fields:
        if field not in data or not data[field]:
            errors[field] = f"{field} is required"
    if 'tags' in data and not isinstance(data['tags'], list):
        errors['tags'] = "Tags must be a list"
    return errors

# Create a new post
@app.route('/posts', methods=['POST'])
def create_post():
    global next_id
    data = request.get_json()  # This is a function in Flask, to transform the data into JSON format
    if not data:
        abort(400, description="Invalid JSON data")  # This is a function in Flask, to abort the request with a specific error message
    errors = validate_post_data(data) 
    if errors:
        return jsonify({"errors": errors}), 400

    new_post = {
        "id": next_id,
        "title": data['title'],
        "content": data['content'],
        "category": data['category'],
        "tags": data['tags'],
        "createdAt": get_current_time(),
        "updatedAt": get_current_time()
    }
    posts.append(new_post)
    next_id += 1
    return jsonify(new_post), 201

# Get all posts
@app.route('/posts', methods=['GET'])
def get_posts():
    term = request.args.get('term', '').lower()
    if term:
        filtered_posts = [
            post for post in posts
            if term in post['title'].lower() or term in post['content'].lower() or term in post['category'].lower()
        ]
    else:
        filtered_posts = posts
    return jsonify(filtered_posts), 200

# Get a specific post by ID
@app.route('/posts/<int:post_id>>', methods=['GET'])
def get_post(post_id):
    post = next((p for p in posts if p['id'] == post_id), None)
    if not post:
        abort(404, description="Post not found")
    return jsonify(post), 200

# Update a post by ID
@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.get_json()
    if not data:
        abort(400, description="Invalid JSON data")
    errors = validate_post_data(data)
    if errors:
        return jsonify({"errors": errors}), 400
    
    post = next((p for p in posts if p['id'] == post_id), None)
    if not post:
        abort(404, description="Post not found")

    post.update({
        "title": data['title'],
        "content": data['content'],
        "category": data['category'],
        "tags": data['tags'],
        "updatedAt": get_current_time()
    })
    return jsonify(post), 200

# Delete a post by ID
@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    global posts
    posts = [p for p in posts if p['id'] != post_id]
    if not posts:
        abort(404, description="Post not found")
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
