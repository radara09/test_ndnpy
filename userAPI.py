import uuid
from flask import Blueprint, request, jsonify
from firebase_admin import firestore

db = firestore.client()
user_Ref = db.collection('user')

userAPI = Blueprint('userAPI', __name__)

@userAPI.route('/add', methods=['POST'])
def create():
    try:   
        id = uuid.uuid4()
        user_Ref.document(id.hex).set(request.json)
        return jsonify({'success': True}), 200
    except Exception as e: 
        return f"an error occured: {e}"
    
@userAPI.route('/list')
def read():
    try: 
        all_users = [doc.to_dict() for doc in user_Ref.stream()]
        return jsonify(all_users), 200
    except Exception as e:
        return f"an error occured: {e}"
    
@userAPI.route('/list/<string:id>', methods=['GET'])
def readOne(id):
    try: 
        user_doc = user_Ref.document(id).get()
        if user_doc.exists:
            user = user_doc.to_dict()
            return jsonify(user), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return f"An error occurred: {e}"

    
@userAPI.route('/update/<string:id>', methods=['PATCH'])
def update(id):
    try:
        user_Ref.document(id).update(request.json)
        return jsonify({'success': True}), 200
    except Exception as e:
        return f"An error occurred: {e}"
    
@userAPI.route('/delete/<string:id>', methods=['DELETE'])
def delete(id):
    try:
        user_Ref.document(id).delete()
        return jsonify({'success': True}), 200
    except Exception as e:
        return f"An error occurred: {e}"