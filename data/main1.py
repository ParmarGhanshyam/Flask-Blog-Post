from datetime import datetime
from flask import Flask, render_template, request,url_for,request,flash,session,redirect,abort
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.secret_key = "Hardik"  
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///ghp.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Contacts(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    phone_num = db.Column(db.String(12), nullable=False)
    msg = db.Column(db.String(120), nullable=False)
    date = db.Column(db.String(12), nullable=True)
    email = db.Column(db.String(20), nullable=False)

class ghp(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    Username = db.Column(db.String(80), unique=True, nullable=False)
    Password = db.Column(db.String(30),nullable = False)

class filedata(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    Title = db.Column(db.String(80), nullable=False)
    Blog = db.Column(db.String(30),nullable = False)
    filename = db.Column(db.BLOB,nullable = True)



@app.route('/')
def home():
    name = "Ghanshyam"
    return render_template('home.html',name = name)

@app.route('/about')
def about(): 
   return render_template('about.html')

@app.route('/index')
def index(): 
   return render_template('index.html')

@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    if(request.method=='POST'):
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        entry = Contacts(name=name, phone_num = phone, msg = message, date= datetime.now(),email = email)
        db.session.add(entry)
        db.session.commit()
    return render_template('contact.html')

@app.route('/post')
def post(): 
   return render_template('post.html')

@app.route('/login',methods = ['GET','POST'])     
def login():
    if request.method == "POST":
        # session['un'] = request.form['un']   
        username = request.form['username']
        passwd = request.form['password'] 
        session['Username'] = username
        print(username,passwd)
        mytodo = ghp.query.filter_by(Username=username,Password= passwd).first()
        if mytodo is not None:
            flash("you have been login sucessfully","info")
            return render_template('dashboard.html',Username = username,Password = passwd)   
        else:
            flash("Not Log in","info")
            return render_template('login.html',Username = username,Password = passwd)
        print(mytodo)     
    mytodo = ghp.query.all()
    return render_template('login.html',mytodo = mytodo)

@app.route('/sign_up',methods = ['GET','POST'])
def sign_up():
    if request.method == "POST":
        uname = request.form['username']
        passwd = request.form['password']
       
        print(uname,passwd)
        try:
            myfunc = ghp(Username = uname,Password = passwd)
            print(myfunc)
            db.session.add(myfunc)
            db.session.commit()
            flash("register Sucessfully","sucess")
            return redirect('/login')
        except Exception as e: 
            flash("Not Register","info")
            return render_template('sign_up.html')
    mydata = ghp.query.all()
    return render_template('sign_up.html',mydata = mydata)

@app.route('/Message')
def Message():
    return render_template('Message.html')

@app.route('/dashboard',methods = ['GET','POST'])
def dashboard():
    alldata = filedata.query.all()
    if request.method == "POST":
        Title1 = request.form['title']
        Blog1 = request.form['blog']
        filename1 = request.files['file']
        print(filename1)
        alldata= filedata(Title = Title1, Blog = Blog1, filename = filename1.read())
        print(alldata)
        db.session.add(alldata)
        db.session.commit()
    if 'Username' in session:
        return render_template('dashboard.html',alldata = alldata)
    else:
        return redirect('/login')  

@app.route('/data')
def data():
    alldata1 = filedata.query.all()
    return render_template('data.html',alldata1=alldata1)

@app.route('/logout')
def logout():
    session.pop('Username', None) 
    return redirect('/')      

if __name__ == '__main__':  
   app.run(debug = True,port = 8000)