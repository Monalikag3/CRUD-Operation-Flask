# Import Libraries
from flask import Flask, render_template, request,redirect, url_for, flash

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# create an object for flask
app = Flask(__name__)
app.secret_key = "Secret Key"


################### Database Configuration #######################

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

####################################################################

#################### Model Creation ############################

class User(db.Model):
    __tablename__ = 'phonebook'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    first_name=db.Column(db.String(60),index=True)
    last_name=db.Column(db.String(60),index=True)
    phone_number = db.Column(db.Integer)
    company = db.Column(db.String(60),index=True)

    def __init__(self, first_name,last_name,email,phone_number,company):
        self.first_name = first_name
        self.last_name = last_name
        self.email=email
        self.phone_number=phone_number
        self.company=company
    def __repr__(self):
        return "first_name- {} and  last_name - {} and email-{} and phone_number-{} and company-{} ".format(self.first_name, self.last_name,self.email,self.phone_number,self.company)

####################################################################
@app.before_first_request
def create_table():
    db.create_all()

#This is the index route where we are going to
#query on all our employee data
@app.route('/')
def Index():
    all_data = User.query.all()

    return render_template("index.html", users = all_data)





@app.route("/add", methods=['GET','POST'])
def add():
    if request.method == 'POST':

        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        company = request.form['company']


        my_data = User(first_name,last_name,email,phone_number,company)
        db.session.add(my_data)
        db.session.commit()
        flash("User Details Inserted Successfully")

        print(first_name)
        print(last_name)
        print("details Added Successfully")
    return redirect(url_for('Index'))

@app.route('/update', methods = ['GET', 'POST'])
def update():

    if request.method == 'POST':
        my_data = User.query.get(request.form.get('id'))

        my_data.first_name = request.form['first_name']
        my_data.last_name = request.form['last_name']
        my_data.email = request.form['email']
        my_data.phone_number = request.form['phone_number']
        my_data.company = request.form['company']

        db.session.commit()
        flash("User Updated Successfully")

        return redirect(url_for('Index'))


@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = User.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("User Details Deleted Successfully")

    return redirect(url_for('Index'))


if __name__=='__main__':
    app.run(debug=True, port=5002) 