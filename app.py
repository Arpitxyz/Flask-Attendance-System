from flask import Flask, redirect, url_for, request, render_template, session, flash

app=Flask(__name__)
app.secret_key="my-secret-key"


user_credentials={
    "admin":"admin123",
    "veronica":"2481"
}

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/details", methods=["Get", "POST"])
def details():
    if request.method=="POST":
        session["first_name"]=request.form.get("first_name")
        last_name=request.form.get("last_name")
        dob=request.form.get("dob")
        email=request.form.get("email")
        gender=request.form.get("gender")
        mobile=request.form.get("mobile")
        return redirect(url_for("register"))
    return render_template("details.html")



@app.route("/register", methods=["Get", "POST"])
def register():
    first_name=session.get("first_name")
    if request.method=="POST":
        username=request.form.get("user_name")
        password=request.form.get("password")
        hint=request.form.get("hint")

        # if username already exists
        if username in user_credentials:
            flash("Username already exists !", "error")
            return render_template("register.html", first_name=first_name)
        
        # Saving the new user
        user_credentials[username]=password

        # Log them in immediately
        session["user"] =username
        flash("Registration successful !", "success")
        return redirect(url_for("success"))
    return render_template("register.html", first_name=first_name)



@app.route("/login", methods=["Get", "POST"])
def login():
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        if username in user_credentials and user_credentials[username]==password:
            session["user"]=username
            return redirect(url_for("success"))
        else:
            flash("Invalid credentials", "error")
            return render_template("login.html")
    return render_template("login.html")



@app.route("/success")
def success():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("success.html")



@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))





if __name__=="__main__":
    app.run(debug=True)
    