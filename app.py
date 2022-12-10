
from flask import Flask, render_template, redirect, session, request, flash
from flask_sqlalchemy import SQLAlchemy
from services.models import *
from flask_cors import CORS
import os



PORT = 5000
DB_FILENAME = 'database.db'
INIT_DB = True  # to create db file


app = Flask(__name__)


def create_app():
    '''
    Creates a flask app

    Returns
    -------
    (app, db): tuple
        has the app object and the db object
    '''
    # create flask app
    app = Flask(__name__)

    # create database extension
    app.secret_key = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '').replace(
        'postgres://', 'postgresql://') or 'sqlite:///' + DB_FILENAME

    print(app.config['SQLALCHEMY_DATABASE_URI'])

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)

    # create flask cors extension
    CORS(app)
    with app.app_context():
        db.create_all()
    return app, db


# create flask app
app, db = create_app()

####################


###############

@app.route('/' )
def index():
    return render_template('home.html')
#########################

@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def post_login():
    username = request.form.get('username')
    password = request.form.get('password')

    query = Users.getByUsername(username)
    if (query == None):
        return "wrong email "

    if query.password != password:
        return "<h1>wrong password</h1>"

    session['username'] = True
    session['uname'] = username

    flash(" login sucess")


    return render_template('home.html')

########## logout 

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")
###############################register ###################


@app.route('/register')
def Get_register():
    return render_template("register.html")


@app.route('/register', methods=['POST'])
def post_reg_page():

    # retrieve input
    name = request.form.get('name')
    username = request.form.get('username')
    password = request.form.get('password')
    # input to database

    users=Users(name = name,username = username,password=password)
    db.session.add(users)
    db.session.commit()
    # clear current session
    session.clear()
    flash("Congratulation you Can login now")
    # redirect to index page
    return redirect('/')
########## send message######

@app.route('/sendmessage')
def send_message():
    
    return render_template("send_message.html")



@app.route('/sendmessage' , methods = ['POST'])
def post_send_message():
    txt = request.form.get('m_txt')
    sender = session['uname']
    reciver = request.form.get('m_reciver')
    
    query = Users.getByUsername(reciver)
    if (query == None):
        return "NOT USER YET"
    else:
        s_message=S_message(txt = txt,sender = sender,reciver=reciver)
        r_message=R_message(txt = txt,sender = sender,reciver=reciver)
        db.session.add(s_message)
        db.session.add(r_message)
        db.session.commit()
        return render_template("send_message.html")

        ########


@app.route('/sent_messages')
def messages():
    if "username" in session:
        username = session['uname']
        
        messgess = Users.get_sent_messages(username)
        return render_template('messages.html' , messgess = messgess )
    else:
        return "login"

#######################

@app.route('/reseved_messages')
def reseved_messages():
    if "username" in session:
        username = session['uname']
        messagess = R_message.query.filter_by(reciver=username)
        return render_template('reseived.html' , messagess = messagess )
    else:
        return "login"

@app.route('/sent_messages/<id>/delete')
def delete_s_message(id):

    S_message.delete(id)

    return redirect('/sent_messages')

@app.route('/reseved_messages/<id>/delete')
def delete_r_message(id):
    R_message.delete(id)

    return redirect('/reseved_messages')
        

############### edite message #######

@app.route('/sent_messages/<id>/edit', methods=['GET'])
def edit_s_message(id):
    message = S_message.get(id).txt
    return render_template('edit_message.html' ,id = id, message = message)


@app.route('/sent_messages/<id>/edit'  , methods=['POST'])
def edit_s_message_post(id):
    txt = request.form.get('m_txt')
    S_message.update(id , txt)
    return redirect('/sent_messages')


#########################################################to run the website####################################################################
if __name__ == "__main__":
    app.run(debug=True, port=PORT, host='0.0.0.0')
