from os import name
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Users(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.BigInteger)
    password = db.Column(db.String(100))


    def __init__(self,name,email,phone,password):
        self.name = name
        self.email = email
        self.phone = phone
        self.password = password


db.create_all()

class UsersSchema(ma.Schema):
    class Meta:
        fields = ('id','name','email','phone','password')


user_schema = UsersSchema()
users_schema = UsersSchema(many=True)

def create_return(id,name,email,phone):
    user_return = {}
    user_return['id'] = id
    user_return['name'] = name
    user_return['email'] = email
    user_return['phone'] = phone

    return user_return

def create_returns(users):
    users_returns = []
    #json_dic = json.loads(users)
    for user in users:
        users_returns.append(create_return(user['id'],user['name'],user['email'],user['phone']))
        print('hola')

    print(users_returns)
    return users_returns


#Endpoint new_user
@app.route('/user', methods=['POST'])
def create_user():
    name = request.json['name']
    email = request.json['email']
    phone = request.json['phone']
    password = request.json['password']
    hashed_pswd = pbkdf2_sha256.hash(password)
    new_user = Users(name,email,phone,hashed_pswd)
    db.session.add(new_user)
    db.session.commit()
   
    return create_return(new_user.id,new_user.name,new_user.email,new_user.phone)


#Endpoint edit_user
@app.route('/user/<id>', methods=['PUT'])
def edit_user(id):
    user = Users.query.get(id)
    name = request.json['name']
    email = request.json['email']
    phone = request.json['phone']
    password = request.json['password']
    hashed_pswd = pbkdf2_sha256.hash(password)
    user.name = name
    user.email = email
    user.phone = phone
    user.password = hashed_pswd
    db.session.commit()

    return create_return(user.id,user.name,user.email,user.phone)


#Enpoint get user
@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    user = Users.query.get(id)

    return create_return(user.id,user.name,user.email,user.phone)


#Endpoint see all users
@app.route('/user', methods=['GET'])
def get_all_users():
    all_users = Users.query.all()
    result = users_schema.dump(all_users)
    
    return jsonify(create_returns(result))


if __name__ == "__main__":
    app.run(debug=True)