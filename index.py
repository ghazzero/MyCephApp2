from flask import Flask, request, render_template, flash
import requests
import json
from flask_wtf import Form
from wtforms import validators,StringField, IntegerField,SubmitField
from flask_cors import CORS,cross_origin

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.secret_key = 'development key'

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
    r = requests.get('http://10.10.6.1:6969/api/v0.1/health.json')
    return render_template('home.html',data =json.loads(r.text))

@app.route('/AddUser')
def adduser():
    r = requests.get('http://10.10.6.1:6969/api/v0.1/auth/list.json')
    return render_template('adduser.html', data =json.loads(r.text))

@app.route('/AddUser/DelUser/<string:entity>')
def deluser(entity):
    return (entity)

@app.route('/AddUser/form', methods = ['GET','PUT'])
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

@app.route('/latihanjson', methods=['GET'])
def latihanjson():
    r = requests.get('http://10.10.6.1:6969/api/v0.1/auth/list.json')
    return render_template('parsing_json.html',data =json.loads(r.text))

if __name__=='__main__':
    app.run(host='0.0.0.0',port=8080,debug=True)
