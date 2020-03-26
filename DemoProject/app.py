from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restplus import Api, fields, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/Demo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = True
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)


class User(db.Model):
    """"
    Creating a User Model

    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80))


class UserSchema(ma.Schema):
    """
    Using marshmallow for serialization and deserialization operations

    """

    class Meta:
        fields = ('id', 'name', 'email', 'password')


"""

  registering models to API

 """
model = api.model('demo', {
    'id': fields.Integer(required=False),
    'name': fields.String('Enter Name'),
    'email': fields.String('Enter Email'),
    'password': fields.String('Enter Password')
})

model1 = api.model('demo1', {
    'id': fields.Integer(required=True),

})

user_schema = UserSchema()
users_schema = UserSchema(many=True)


class UserView(Resource):
    """
    Creating a view to get,update,delete, creating a record in the data base

    """

    def get(self):

        return jsonify(users_schema.dump(User.query.all()))

    @api.expect(model)
    def post(self):

        user = User(name=request.json['name'], email=request.json['email'], password=request.json['password'])
        db.session.add(user)
        db.session.commit()
        return {'message': 'data added to database'}

    @api.expect(model)
    def put(self):

        id = request.json['id']
        user = User.query.get(id)
        user.name = request.json['name']
        user.email = request.json['email']
        user.password = request.json['password']
        db.session.commit()
        return {'message': 'data updated'}

    @api.expect(model1)
    def delete(self):

        id = request.json['id']
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return {'message': 'data deleted successfully'}


api.add_resource(UserView, '/MyApi')

if __name__ == '__main__':
    app.run(debug=True)
