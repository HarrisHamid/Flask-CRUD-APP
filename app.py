from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\harri\\Documents\\GitHub\\Flask-CRUD-APP\\instance\\UserData.db'

app.secret_key = 'secret key'  # Change this to a more secure secret key
db = SQLAlchemy(app)

# Creating Tables
class UserData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True) 
    access = db.Column(db.String(100))

    def __init__(self, name, email, access):
        self.name = name
        self.email = email
        self.access = access


@app.route('/')
def Index():
    all_data = UserData.query.all()
    return render_template("index.html", users=all_data)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        access = request.form['access']

        my_data = UserData(name, email, access)
        db.session.add(my_data)
        db.session.commit()

        flash("User Insertion Successful")

        return redirect(url_for('Index'))


@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        data_id = request.form.get('id')
        my_data = UserData.query.get(data_id)

        if my_data:
            my_data.name = request.form['name']
            my_data.email = request.form['email']
            my_data.access = request.form['access']

            db.session.commit()
            flash("User Update Successful")
        else:
            flash("User with the provided ID does not exist")

        return redirect(url_for('Index'))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
