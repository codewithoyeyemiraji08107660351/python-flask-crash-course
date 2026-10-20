from flask import Flask, request 

#URL Paramter
app = Flask(__name__)

@app.route("/users/<username>")
def get_username(username):
    return f"Hello {username}"


@app.route("/users/<int:id>")
def get_userid(id):
    return f"User ID: {id}"

#Query Parameters
@app.route("/products", method=["GET"])
def get_product():
    name = request.args.get("name")
    price = request.args.get("price")
    return f"Product Name: {name}, Price: {price}"


@app.route("/products", method=["POST"])
def create_product():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")

    return {
        "name":name,
        "email":email
    }
#Http Status codes

if __name__ == "__main__":
    app.run(debug=True)
