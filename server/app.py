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

@app.route('/')
def index():
    return '<h1>Frontend & Backend</h1>'

@app.route('/messages', methods = ['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = [message.to_dict() for message in Message.query.order_by(Message.created_at.asc()).all()]
        response = make_response(
            jsonify(messages),
            200
            )

        return response
    
    elif request.method =="POST":
        
        data = request.json

        if 'body' in data and 'username' in data:
            new_message = Message(body =data['body'], username = data['username'])

            db.session.add(new_message)
            db.session.commit()

            message_dict = new_message.to_dict()
            response = make_response(
                jsonify(message_dict),
                201
            )

            return response

@app.route('/messages/<int:id>', methods =['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()

    if request.method == 'PATCH':


        for attr in request.json:
            setattr(message, attr, request.json.get(attr))
            
        db.session.add(message)
        db.session.commit()

        message_dict = message.to_dict()
        response = make_response(
            jsonify(message_dict),
                200
            )
        response.headers["Content-Type"]= "application/json"
        return response
    
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()

        response_body ={
            "Delete Successful": True,
            "Message": "Message Deleted"
        }

        response = make_response(
            jsonify(response_body),
            200
        )
        return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
