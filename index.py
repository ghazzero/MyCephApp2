from flask import Flask, request, render_template, flash
from data import Users
from flask_wtf import Form
from wtforms import validators,StringField, IntegerField,SubmitField


app = Flask(__name__)
app.secret_key = 'development key'
users = Users()

class BuatUser(Form):
    userID = StringField('userID', validators=[validators.length(min=4,max=25)])
    OSDcap = StringField('OSDcap', validators=[validators.length(min=0,max=3)])
    MONcap = StringField('MONcap', validators=[validators.length(min=0,max=3)])
    MDScap = StringField('MDScap', validators=[validators.length(min=0,max=3)])
    submit = SubmitField()

class BuatVolume(Form):
    poolID = IntegerField('PoolID')
    capacity = IntegerField('capacity')
    submit = SubmitField()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/AddUser')
def adduser():
    return render_template('adduser.html', users = users)

@app.route('/AddUser/form', methods = ['GET','POST'])
def adduserform():
    form = BuatUser(request.form)
    if request.method == 'POST':
        if form.validate() == False:
            flash('Isi seluruhnya')
            return render_template('form.html', form=form)
        else:
            return render_template('success.html')
    elif request.method == 'GET':
        return render_template('form.html', form=form)


@app.route('/AddVolume',methods = ['GET','POST'])
def addvolume():
    form = BuatVolume(request.form)
    if request.method == 'POST':
        if form.validate() == False:
            flash('Isi seluruhnya')
            return render_template('addvolume.html', form=form)
        else:
            return render_template('success.html')
    elif request.method == 'GET':
        return render_template('addvolume.html', form=form)

@app.route('/LinkUserVolume')
def linkuservolume():
    return render_template('home.html')

if __name__=='__main__':
    app.run(port=8080,debug=True)