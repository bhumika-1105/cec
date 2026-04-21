from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "secret123"

users = []

def auth():
    return session.get("username")


# LOGIN
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["username"] = request.form["username"]
        session["msg"] = "Login Successful 🎉"
        return redirect("/dashboard")
    return render_template("login.html", msg=session.pop("msg", None))


# DASHBOARD
@app.route("/dashboard")
def dashboard():
    if not auth():
        return redirect("/")
    return render_template(
        "dashboard.html",
        username=session["username"],
        user_count=len(users),
        msg=session.pop("msg", None)
    )


# CREATE
@app.route("/create", methods=["GET", "POST"])
def create():
    if not auth():
        return redirect("/")

    if request.method == "POST":
        users.append({
            "name": request.form["name"],
            "phone": request.form["phone"],
            "email": request.form["email"],
            "password": request.form["password"]
        })

        session["msg"] = "User Created 💖"
        return redirect("/userlist")

    return render_template("create.html")


# USERLIST
@app.route("/userlist")
def userlist():
    if not auth():
        return redirect("/")

    return render_template(
        "userlist.html",
        users=users,
        edit_id=request.args.get("edit", type=int),
        msg=session.pop("msg", None)
    )


# UPDATE INLINE
@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    users[id]["name"] = request.form["name"]
    users[id]["phone"] = request.form["phone"]
    users[id]["email"] = request.form["email"]
    users[id]["password"] = request.form["password"]

    session["msg"] = "Updated ✏️"
    return redirect("/userlist")


# DELETE
@app.route("/delete/<int:id>")
def delete(id):
    if auth():
        users.pop(id)
        session["msg"] = "Deleted ❌"
    return redirect("/userlist")


# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)