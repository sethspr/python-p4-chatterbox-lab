from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        all_messages = Message.query.all()

        message_dict = []
        for message in all_messages:
            message_dict.append(message.to_dict())
        return message_dict, 200
    
    elif request.method == 'POST':
        json_data = request.get_json()
        new_msg = Message(
            body=json_data.get('body'),
            username=json_data.get('username'),
        )

        db.session.add(new_msg)
        db.session.commit()

        return new_msg.to_dict(), 201

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    msg_obj = Message.query.filter(Message.id == id).first()

    if msg_obj is None:
        return {'Error': f'{id} not found'}, 404
    
    if request.method == 'PATCH':
        json_data = request.get_json()
        
        for field in json_data:
            value = json_data[field]
            setattr(msg_obj, field, value)

        db.session.add(msg_obj)
        db.session.commit()

        return msg_obj.to_dict(), 200
    
    elif request.method == 'DELETE':
        db.session.delete(msg_obj)
        db.session.commit()

        return {}, 204


if __name__ == '__main__':
    app.run(port=5555)
