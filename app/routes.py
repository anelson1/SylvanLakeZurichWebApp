from flask import *
from app import app,db
from app.form import *
from flask_bootstrap import Bootstrap
from app.database import User
from flask_login import current_user, login_user, login_required, logout_user
import os
from pathlib import Path
bootstrap = Bootstrap(app)

@app.route("/")
@login_required
def index():
    user = User.query.get(current_user.id)
    if user.username == 'admin':
        return redirect(url_for("admin"))
    else:
        return redirect(url_for('program',programname = user.classType))

@app.route("/<programname>")
@login_required
def program(programname):
    form = signout()
    user = User.query.get(current_user.id)
    if user.username == 'admin':
        return redirect(url_for("admin"))
    
    files = os.listdir(str(os.getcwd()) + '\\app\\static\\data\\' + programname)
    routeurl = programname
    print(programname)
    return render_template("home.html", form=form, name=user.name, programname=user.classType, files=files, routeurl = routeurl)

@app.route("/<programname>/<level>")
@login_required
def fileselect(programname, level):
    form = signout()
    user = User.query.get(current_user.id)
    if user.username == 'admin':
        return redirect(url_for("admin"))
    url = str(os.getcwd()) + '\\app\\static\\data\\'+programname + "\\"+level
    files = os.listdir(url)
    routeurl = url_for('fileselect',programname = programname, level = level)
    for f in files:
        print(routeurl + "/" + f)
    return render_template("home.html", form=form, name=user.name, programname=user.classType, files=files, routeurl = routeurl)

@app.route("/<programname>/<level>/<filename>")
@login_required
def fileDisplay(programname, level,filename):
    form = signout()
    user = User.query.get(current_user.id)
    if user.username == 'admin':
        return redirect(url_for("admin"))
    url = str(os.getcwd()) + '\\app\\static\\data\\'+programname + "\\"+level
    files = os.listdir(url)
    return redirect(url_for('static', filename='data/'+programname + "/" + level + "/" + filename) )
        
@app.route("/admin")
@login_required
def admin():
    created = request.args.get('created')
    name = request.args.get('name')
    classType = request.args.get('classType')
    error = request.args.get('err')
    form = registerform()
    user = User.query.get(current_user.id)
    if user.username != 'admin':
        redirect(url_for('index'))
    print(user.username, user.password)
    return render_template("admin.html", form=form, created=created, err= error,name=name,classType=classType)

@app.route("/students")
@login_required
def students():
    if current_user.username != 'admin':
        redirect(url_for('index'))
    students = User.query.all()
    return render_template("students.html", studentlist = students)
      
@app.route("/login", methods=['GET'])
def login():
    error = request.args.get('uErr')
    
    print(error)
    form = loginform()
    return render_template("index.html", uErr=error, form=form)

@app.route("/teacherlogin", methods=['GET'])
def teacherlogin():
    error = request.args.get('uErr')
    print(error)
    form = loginform()
    return render_template("teacherlogin.html", uErr=error, form=form)

@app.route("/loginhandler", methods=['POST'])
def loginhandler():
    username = request.form['username']
    password = request.form['password']
    try:
        remember = request.form['remember']
    except:
        remember = False
    u = User.query.filter_by(username=username).first()
    if not u:
        flash("Error")
        return redirect(url_for("login", uErr=True))
    if u.password == password:
        login_user(u, remember=remember)
        if u.username == 'admin':
                return redirect(url_for("admin"))
        return redirect(url_for("index"))
    else:
        flash("Error")
        return redirect(url_for("login", uErr=True))

@app.route("/adminhandler", methods=['POST'])
@login_required
def adminhandler():
    username = request.form['username']
    password = request.form['password']
    name = request.form['name']
    classType = request.form['classType']
    u = User(username=username, password=password, name=name, classType=classType)
    db.session.add(u)
    try:
        db.session.commit()
    except:
        return redirect(url_for('admin',err=True))
    return redirect(url_for('admin',created=True, name = name, classType = classType))

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
