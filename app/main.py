
from flask import Flask, make_response, request, jsonify
from flask_mongoengine import MongoEngine
from flasgger import Swagger, swag_from

from app import oauth2  # Takes care of setting the JWT stuff


app = Flask(__name__)
swagger = Swagger(app)

#Setting up my mongoDB database using mongo engine
database_name = "API"
DB_URI = f"mongodb+srv://chibuoyim:Chiboy17@cluster0.bfuycr8.mongodb.net/{database_name}?retryWrites=true&w=majority"
app.config["MONGODB_HOST"] = DB_URI

db = MongoEngine()
db.init_app(app)

# Setting up my models

class User(db.Document):
    id = db.SequenceField(primary_key=True)
    first_name = db.StringField(max_length=30, required=True)
    last_name = db.StringField(max_length=30, required=True)
    email = db.StringField(max_length=50, required=True)
    password = db.StringField(required=True)

    def to_json(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password
        }


class Template(db.Document):
    id = db.SequenceField(primary_key=True)
    template_name = db.StringField(required=True)
    subject = db.StringField(required=True)
    body = db.StringField(required=True)
    owner_id = db.IntField(requuired=True)

    def to_json(self):
        return {
            "id": self.id,
            "template_name": self.template_name,
            "subject": self.subject,
            "body": self.body
        }

@swag_from("register_doc.yml")  # swagger documentation
@app.route("/register", methods=["POST"])
def register():
    user_credentials = request.json
    user = User(**user_credentials)  # This unpacks the json into the model and sets each field correctly
    user.save()
    
    return make_response("Sucessfully created user", 201)

@swag_from("login_doc.yml")  # swagger documentation
@app.route("/login", methods=["POST"])
def login():
    user_credentials = request.json
    user = User.objects(email=user_credentials["email"]).first()
    if not user:
        return make_response("Invalid Credentials", 403)
    if user.password != user_credentials["password"]:
        return make_response("Invalid Credentials", 403)


    access_token = oauth2.create_access_token(data = {"id": user.id}) # creates a token
    return {"access_token": access_token, "token_type": "bearer"} # return token


@app.route("/template", methods=["POST", "GET"])
def template():
    try:
        token = request.headers["authorization"][7:len(request.headers["authorization"])]  # Slicing to get the token
        id = oauth2.verify_access_token(token=token)
        if not id:
            return make_response("You are not logged in!", 401)
    except KeyError:
        return make_response("You are not logged in!", 401)
    if request.method == "GET":
        templates = Template.objects(owner_id=id).all()
        return make_response(jsonify(templates), 200)
    else:
        template_info = request.json
        template_info["owner_id"] = id
        template = Template(**template_info)
        template.save()
        return make_response(jsonify(template.to_json()), 201)


@app.route("/template/<int:template_id>", methods=["GET", "PUT", "DELETE"])
def template_one(template_id):
    try:
        token = request.headers["authorization"][7:len(request.headers["authorization"])]
        id = oauth2.verify_access_token(token=token)
        if not id:
            return make_response("You are not logged in!", 401)
    except KeyError:
        return make_response("You are not logged in!", 401)

    if request.method == "GET":

        template = Template.objects(id=template_id).first()
        if not template:
            return make_response(f"Template with id {id} does not exist", 404)
        if template.owner_id != id:
            return make_response("Not authorized to perform requested action", 403)

        return make_response(jsonify(template.to_json()), 200)

    elif request.method == "PUT":
        template_info = request.json
        template = Template.objects(id=template_id).first()
        if not template:
            return make_response(f"Template with id {id} does not exist", 404)
        if template.owner_id != id:
            return make_response("Not authorized to perform requested action", 403)
        template.update(**template_info)
        return make_response(jsonify(template.to_json()), 200)

    else:
        template = Template.objects(id=template_id).first()
        if not template:
            return make_response(f"Template with id {id} does not exist", 404)
        if template.owner_id != id:
            return make_response("Not authorized to perform requested action", 403)

        template.delete()
        return make_response("", 204)


@app.route("/")
def root():
    return {"message": "Hello, world!"}



if __name__ == "__main__":
    app.run(debug=False)