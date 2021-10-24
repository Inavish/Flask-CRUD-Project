from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy, request
from sqlalchemy.sql import text


app = Flask(__name__)


# app.config[url] = value
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Inavish15@localhost/cars'
db = SQLAlchemy(app)


class Car(db.Model):
    Id = db.Column(db.Integer, primary_key=True, unique=True)
    carName = db.Column(db.String(20), primary_key=False)
    carPrice = db.Column(db.String(20), unique=False, nullable=False)
    carColor = db.Column(db.String(20), unique=False, nullable=False)



@app.route("/")
def display():
    sql = text('select * from car')
    result = db.engine.execute(sql)

    return render_template("index.html", car=result)


@app.route("/insert", methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        carName = request.form.get('carName')
        carPrice = request.form.get('carPrice')
        carColor = request.form.get('carColor')

        entry = Car(carName= carName, carPrice=carPrice, carColor=carColor)
        db.session.add(entry)
        db.session.commit()

    return redirect(url_for('display'))


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Car.query.get(request.form.get('id'))

        my_data.carName = request.form['carName']
        my_data.carPrice = request.form['carPrice']
        my_data.carColor = request.form['carColor']

        db.session.commit()

        return redirect(url_for('display'))


@app.route('/delete', methods = ['GET', 'POST'])
def carDelete():
    if request.method == 'POST':
        iid = request.form.get('Id')
        my_data = Car.query.get(iid)
        db.session.delete(my_data)
        db.session.commit()

    return redirect(url_for('display'))

    # iid = request.form.get('id')
    # smtp = Car.query.filter_by(id=id).first()
    # if request.method == 'POST':
    #     if smtp:
    #         db.session.delete(smtp)
    #         db.session.commit()
    #         return redirect('/delete')
    #
    # return redirect(url_for('display'))
        # iid = request.form.get('id')
        #
        # obj = Car.query.filter(Car.id == iid).delete()
        # db.session.delete(obj)
        # db.session.commit()

    # return render_template("index.html")



if __name__ == '__main__':

    app.run(debug = True)
