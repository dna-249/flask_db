from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, reqparse , fields, Api, marshal_with ,abort
from flask_cors import cross_origin,CORS

app = Flask(__name__)
CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///data.db'
db = SQLAlchemy(app)
api = Api(app)

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name =db.Column(db.String, unique = True, nullable= False)
    email =db.Column(db.String, unique = True, nullable= False)
    
    def __repr__(self):
        return f"User(id = {self.id},name = {self.name}, email = {self.email})"
    
user_args = reqparse.RequestParser()
user_args.add_argument("name", type=str,required=True,help="name cannot be found")   
user_args.add_argument("email", type= str,required=True,help="email cannot be found")   

userFields ={
    "id":fields.Integer,
    "name":fields.String,
    "email":fields.String
}

class User(Resource):
    
    @marshal_with(userFields)
    def get(self):
        users = UserModel.query.all()
        return users
    
    
    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(name=args["name"], email=args["email"])
        db.session.add(user)
        db.session.commit()
        user=UserModel.query.all()
        return user, 201
    
api.add_resource(User,"/api/users")
        

        
@app.route("/")

def nur():
    return "hello"

if __name__ == "__main__":
    app.run()