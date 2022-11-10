import os
from flask import Flask, jsonify, request
from model import db, User
from flask_cors import CORS
from flask_migrate import Migrate

BASEDIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///"+\
    os.path.join(BASEDIR,"db.db")

Migrate(app, db)
db.init_app(app)
CORS(app)

@app.route('/users',methods=['GET'])
def get_users():
    users = User.query.all()
    list_users = list()
    for user in users:
        print("user ",user)
        print("user name ", user.name)
        print("user mail ", user.email)
        list_users.append({"name":user.name,"email":user.email})
    print(users)
    return jsonify({"users":list_users})

@app.route('/user/<int:id>',methods=['GET'])
def get_user(id):
    user= User.query.get(id)
    print(user)
    if user is not None:
        return jsonify(user.serialize()),200
    else:
        return jsonify({"msg":"user not found"}),404

@app.route('/user',methods=['POST'])
def inser_user():
    try:
        user= User()
        user.name = request.json.get("name")
        user.email = request.json.get("email")
        if user.name  is not None and user.email is not None:
            db.session.add(user)
            db.session.commit()
            return jsonify({"msg":"ok"})
        else:
            return jsonify({"msg":"bad request"}),500
    except Exception as e:
        return jsonify({"msg":"ups! error server"}),500

@app.route('/delete/<int:id>',methods=['DELETE'])
def delete_user(id):
    try:
        user=User.query.get(id)
        if user is not None:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"msg": "element delete success"})
        else:
            return jsonify({"msg":"bad request"}),500
    except Exception as e:
        return jsonify({"msg":"ups! error server"}),500

@app.route('/update/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        user=User.query.get(id)
        insert_name= request.json.get("name")
        if user is not None:
            user.name=insert_name
            db.session.commit()
            return jsonify({"msg":"ok"})

        else:
            return jsonify({"msg":"bad request"}),500
    except Exception as e:
        return jsonify({"msg":"ups! error server"}),500
    


if __name__== "__main__":
    app.run(debug=True)