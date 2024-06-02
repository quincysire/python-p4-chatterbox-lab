# server/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

migrate = Migrate(app, db)


with app.app_context():
    db.create_all()



@app.route('/messages', methods=['GET'])
def get_messages():
    
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([message.serialize() for message in messages])

@app.route('/messages', methods=['POST'])
def create_message():
    
    data = request.get_json()
    new_message = Message(body=data['body'], username=data['username'])
    db.session.add(new_message)
    db.session.commit()
    return jsonify(new_message.serialize()), 201  

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
  
    message = db.session.query(Message).get(id)
    if message:
        data = request.get_json()
        message.body = data['body']
        db.session.commit()
        return jsonify(message.serialize())
    else:
        return jsonify({'error': 'Message not found'}), 404

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = db.session.query(Message).get(id)
    if message:
        db.session.delete(message)
        db.session.commit()
        return jsonify({'message': 'Message deleted successfully'})
    else:
        return jsonify({'error': 'Message not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)