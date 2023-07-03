import uuid
from flask import Blueprint, request, jsonify
from firebase_admin import firestore

db = firestore.client()
data_Ref = db.collection('data')

dataAPI = Blueprint('dataAPI', __name__)

@dataAPI.route('/test')
def test():
    return{"haloo": ["rahmat", "22"]}

@dataAPI.route('/addData', methods=['POST'])
def create():
    try:   
        id = uuid.uuid4()
        data_Ref.document(id.hex).set(request.json)
        return jsonify({'success': True}), 200
    except Exception as e: 
        return f"an error occured: {e}"
    
@dataAPI.route('/list')
def read():
    try: 
        all_data = [doc.to_dict() for doc in data_Ref.stream()]
        return jsonify(all_data), 200
    except Exception as e:
        return f"an error occured: {e}"
    
@dataAPI.route('/list/<string:id>', methods=['GET'])
def readOne(id):
    try: 
        data_doc = data_Ref.document(id).get()
        if data_doc.exists:
            data = data_doc.to_dict()
            return jsonify(data), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        return f"An error occurred: {e}"
    
@dataAPI.route('/update/<string:id>', methods=['PATCH'])
def update(id):
    try:
        data_Ref.document(id).update(request.json)
        return jsonify({'success': True}), 200
    except Exception as e:
        return f"An error occurred: {e}"
    
@dataAPI.route('/delete/<string:id>', methods=['DELETE'])
def delete(id):
    try:
        data_Ref.document(id).delete()
        return jsonify({'success': True}), 200
    except Exception as e:
        return f"An error occurred: {e}"