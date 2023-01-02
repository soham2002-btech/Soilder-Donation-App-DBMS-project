from flask import Flask,render_template,request,session,redirect
from flask_sqlalchemy import SQLAlchemy # This is to connect Database to front-end
from flask_login import UserMixin,login_user,logout_user,login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required , current_user
from flask_login.login_manager import LoginManager
from flask import url_for
from flask import Flask, send_from_directory
flag = 0
local_server = True 
app = Flask(__name__)
app.secret_key = 'dbmsproject' 
#  For images
# @app.route('/<path:path>', methods=['GET'])
# def static_proxy(path):
#   return send_from_directory('./images', path)

# picFolder = os.path.join('templates','images')
# app.config(['UPLOAD_FOLDER']) = picFolder

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/army'
db=SQLAlchemy(app)


login_manager = LoginManager(app)
login_manager.login_view = 'signin'


class Signup(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30))
    password = db.Column(db.String(100))

class Soldier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    birthdate = db.Column(db.String(100))
    memorialday = db.Column(db.String(100))
    decription = db.Column(db.String(100))
    types = db.Column(db.String(100))
    address = db.Column(db.String(100))
    city = db.Column(db.String(30))
    zipcode = db.Column(db.Integer)

    




@login_manager.user_loader
def load_user(signup_id):
    return Signup.query.get(int(signup_id))


@app.route("/")
def index():    
    return render_template('index.html')

# This id for soldier

@app.route("/addsoldier" , methods=['POST','GET'])
def addsoldier():
    if request.method=="POST":
        flag = 2
        name=request.form.get('name')
        email=request.form.get('email')
        birthdate = request.form.get('birthdate')
        memorialday = request.form.get('memorialday')
        type = request.form.get('type')
        desc = request.form.get('desc')
        address = request.form.get('address')
        city = request.form.get('city')
        zipcode = request.form.get('zipcode')
        new_user = db.engine.execute(f"INSERT INTO `soldier` ( `name`, `email`,`birthdate`, `memorialday`, `description`, `type`, `addresss`, `city`, `zipcode`) VALUES ( '{name}','{email}', '{birthdate}', '{memorialday}', '{desc}', '{type}', '{address}', '{city}', '{zipcode}');")

        print("This is  Post Buddy")
        

    if request.method=="GET":
        flag = 1
        print("This is get method")
        
    return render_template('addsoldier.html')

@app.route("/test")
def test():
    try:
        Notes.query.all()
        return 'Success'
    except:
        return 'Fail to connect'



@app.route("/contactus")
def contactus():
    return render_template('contactus.html')


@app.route("/signup" , methods=['POST','GET'])
def signup():
    if request.method=="POST":
        email=request.form.get('email')
        password=request.form.get('password')
        print("email =" , email)
        print("Password = " , password)

        user=Signup.query.filter_by(email=email).first()
        if user:
            print("Email already existed")
            return render_template('/signup.html')

        else:
            encpassord = generate_password_hash(password)
            print("Stm 1")
            # new_user = db.engine.execute(f" INSERT INTO 'user' ('username','email','password') VALUES ('{username}' , '{email}' , '{encpassord}');")
            new_user = db.engine.execute(f"INSERT INTO `signup` (`email`, `password`) VALUES ('{email}', '{password}');")
            print("Stm 2")
            return render_template('signin.html')
    # print("Method = ")
    # print(request.method)


    return render_template('signup.html')


@app.route("/new_index",methods=['POST','GET'])
@login_required
def new_index():
    # print("Catagory ",catagory)
    if request.method=="POST":
        print(" This is POST")
        return render_template('new_index.html')
    else:
        print(" This is GET")

        return render_template('new_index.html')


@app.route("/logout")
@login_required
def logout():
    flag = 0
    logout_user()
    return redirect(url_for('signin'))



@app.route("/showarmy")
def showarmy():
    query = db.engine.execute("SELECT * FROM `soldier` WHERE type='army'")
    return render_template('showarmy.html', query=query)

@app.route("/shownavy")
def shownavy():
    query = db.engine.execute("SELECT * FROM `soldier` WHERE type='navy'")
    return render_template('shownavy.html', query=query)

@app.route("/showairforce")
def showairforce():
    query = db.engine.execute("SELECT * FROM `soldier` WHERE type='airforce'")
    return render_template('showairforce.html', query=query)



@app.route("/signin", methods=['POST','GET'])
def signin():
    if request.method=="POST":
        email=request.form.get('email')
        password=request.form.get('password')
        user = Signup.query.filter_by(email=email).first()
        if user and user.password==password:
            print(" You can proceed :) ")
            login_user(user)
            return redirect(url_for('new_index'))
        else:
            print("Invalid details")
            return render_template('signin.html')

        print(email , password)
        return render_template('signin.html')
    return render_template('signin.html')  
    
    return render_template('signin.html')

# @app.route("/signup")
# def signup():
#     return render_template('signup.html')
print("flag = ",flag)

app.run(debug=True , threaded=True)
