from quart import Quart, request, render_template
from quart.templating import render_template
from mongodc import Client

app = Quart(__name__)
client = Client()

@app.route("/", methods=["GET", "POST"])
async def index():
    data = client.read_all_users()
    return await render_template("index.html", users=data)

@app.route("/create", methods=["GET", "POST"])
async def create():
    if request.method == "POST":
        form = await request.form
        name = form["name"]
        number = form["number"]
        email = form["email"]
        client.create_user(
            {
                "name": name,
                "number": number,
                "email": email
            }
        )
        return await index()
        
    return await render_template("create.html")

@app.route("/view")
async def view():
    return await render_template("view.html")

@app.route("/edit")
async def edit():
    return await render_template("edit.html")


app.run(debug=True)
