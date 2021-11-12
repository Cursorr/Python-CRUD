from quart import Quart, request, render_template, make_response
from quart.templating import render_template
from werkzeug.utils import redirect
from mongodc import Client
from functools import wraps

import datetime
import secrets
import jwt 
import hashlib

app = Quart(__name__)
app.config["SECRET_KEY"] = secrets.token_urlsafe(16)
hashedvalue = hashlib.new('sha512_256')
client = Client()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token') 

        if not token:
            return {"Code": "403", "Error": "Acces Forbidden"} 

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return {"Code": "403", "Error": "Acces Forbidden"} 

        return f(*args, **kwargs)

    return decorated

@app.route("/", methods=["GET", "POST"])
async def index():
    if request.method == "POST":
        form = await request.form
        password = form["password"]
        hashedvalue.update(bytes(password, "utf-8"))
        credentials = client.major["connect"].find_one({"username": "admin"})
        if hashedvalue.hexdigest() == credentials["password"]:
            jwt.encode({'user' : "admin", 'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=15)}, app.config['SECRET_KEY'])
            return redirect("/users/")
            
    return await render_template("index.html")

@app.route("/users/")
@token_required
async def users():
    data = client.read_all_users()
    return str(data)

@app.route("/users/<_id>/")
@token_required
async def get_user_data(_id):
    try:
        user = client.read_user({"_id": int(_id)})
    except:
        return {"Code": "404", "Error": "User not found"} 

    return str(user)
    
@app.route("/users/create", methods=["GET", "POST"])
@token_required
async def create():
    if request.method == "POST":
        form = await request.form
        name = form["name"]
        number = form["number"]
        email = form["email"]
        data = client.create_user(
            {
                "name": name,
                "number": number,
                "email": email
            }
        )
        return redirect(f"/users/{data['_id']}/")
            
    return await render_template("create.html")

@app.route("/users/<_id>/update/", methods=["GET", "POST"])
@token_required
async def update(_id):
    try:
        user = client.read_user({"_id": int(_id)})
    except:
        return {"Code": "404", "Error": "User not found"} 
    
    if user is None:
        return str(user)
    
    if request.method == "POST":    
        form = await request.form
        name = form["name"]
        number = form["number"]
        email = form["email"] 
        client.update_user(
            [int(_id), {"name": name, "number": number, "email": email}]
        )
        return redirect(f"/users/{_id}/")
            
    return await render_template("update.html", user=user)
        
@app.route("/users/<_id>/delete/", methods=["GET", "POST"])
@token_required
async def delete(_id):
    try:
        user = client.read_user({"_id": int(_id)})
    except:
        return {"Code": "404", "Error": "User not found"} 
    
    if user is None:
        return str(user)
                   
    if request.method == "POST":
        client.delete_user({"_id": int(_id)})
        return redirect("/users/")
    
    return await render_template("delete.html")
    
@app.route("/users/clear/", methods=["GET", "POST"])
@token_required
async def clear():
    if request.method == "POST":
        client.delete_all()
        return redirect("/users/")
    
    return await render_template("delete.html")

app.run(debug=True)
