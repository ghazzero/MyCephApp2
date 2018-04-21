from flask import Flask, request, render_template, flash, redirect
import requests
import json
from flask_wtf import Form
from wtforms import validators,StringField, IntegerField,SubmitField, BooleanField
from flask_cors import CORS,cross_origin

app = Flask(__name__)
cors = CORS(app, resources={r"10.10.6.251:5000/api/v0.1/*": {"Access-Control-Allow-Origin": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.secret_key = 'development key'
headers = {'Access-Control-Max-Age' : '3600',
           'Content-Type' : 'text/plain',
           'Content-Length' : '0',
           'Access-Control-Allow-Origin': '*',
           "Access-Control-Allow-Credentials": "True",
           'Access-Control-Allow-Methods': 'GET, POST, OPTIONS,PUT',
           'Access-Control-Allow-Headers': 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range',
           'Access-Control-Expose-Headers': 'Content-Length'}

def PilihCapsMon(r,w,x):
    if r == True and w ==True and x == True:
        return "mon", "allow rwx"
    elif r == True and w == True and x == False:
        return "mon", "allow rw"
    elif r == True and w == False and x == True:
        return "mon", "allow rx"
    elif r == True and w == False and x == False:
        return "mon", "allow r"
    elif r == False and w == True and x == True:
        return "mon", "allow wx"
    elif r == False and w == False and x == True:
        return "mon", "allow x"
    elif r == False and w == True and x == False:
        return "mon", "allow w"
    elif r == False and w == False and x == False:
        return None

def PilihCapsOsd(r,w,x):
    if r == True and w ==True and x == True:
        return "osd", "allow rwx"
    elif r == True and w == True and x == False:
        return "osd", "allow rw"
    elif r == True and w == False and x == True:
        return "osd", "allow rx"
    elif r == True and w == False and x == False:
        return "osd", "allow r"
    elif r == False and w == True and x == True:
        return "osd", "allow wx"
    elif r == False and w == False and x == True:
        return "osd", "allow x"
    elif r == False and w == True and x == False:
        return "osd", "allow w"
    elif r == False and w == False and x == False:
        return None 

def PilihCapsMds(r,w,x):
    if r == True and w ==True and x == True:
        return "mds", "allow rwx"
    elif r == True and w == True and x == False:
        return "mds", "allow rw"
    elif r == True and w == False and x == True:
        return "mds", "allow rx"
    elif r == True and w == False and x == False:
        return "mds", "allow r"
    elif r == False and w == True and x == True:
        return "mds", "allow wx"
    elif r == False and w == False and x == True:
        return "mds", "allow x"
    elif r == False and w == True and x == False:
        return "mds", "allow w"
    elif r == False and w == False and x == False:
        return None    

class BuatUser(Form):
    userID = StringField('userID')
    OSDr   = BooleanField('read')
    OSDw   = BooleanField('write')
    OSDx   = BooleanField('execute')
    MONr   = BooleanField('read')
    MONw   = BooleanField('write')
    MONx   = BooleanField('execute')
    MDSr   = BooleanField('read')
    MDSw   = BooleanField('write')
    MDSx   = BooleanField('execute')
    submit = SubmitField()

class BuatVolume(Form):
    poolID = IntegerField('PoolID')
    capacity = IntegerField('capacity')
    submit = SubmitField()

@app.route('/')
def index():
    r = requests.get('http://10.10.6.251:5000/api/v0.1/health.json')
    return render_template('home.html',data =json.loads(r.text),headers=headers)

@app.route('/AddUser')
def adduser():
    r = requests.get('http://10.10.6.251:5000/api/v0.1/auth/list.json')
    return render_template('adduser.html', data =json.loads(r.text),headers=headers)

@app.route('/AddUser/DelUser/<string:entity>', methods = ['GET','PUT'])
def deluser(entity):
    requests.put('http://10.10.6.251:5000/api/v0.1/auth/del', params={"entity":entity},headers=headers)
    return redirect('/AddUser')

@app.route('/AddUser/form', methods = ['GET','POST','PUT'])
def adduserform():
    form = BuatUser(request.form)
    if request.method == 'POST':
        if form.validate() == False:
            flash('Isi seluruhnya')
            return render_template('form.html', form=form)
        else:
            requests.put('http://10.10.6.251:5000/api/v0.1/auth/get-or-create',
                params={"entity":"client."+form.userID.data, "caps":[ 
                PilihCapsMon(form.MONr.data,form.MONw.data,form.MONx.data),
                PilihCapsOsd(form.OSDr.data,form.OSDw.data,form.OSDx.data),
                PilihCapsMds(form.MDSr.data,form.MDSw.data,form.MDSx.data)]},headers=headers)
            return redirect('/AddUser')
    elif request.method == 'GET':
        return render_template('form.html', form=form)

@app.route('/AddUser/EditUser/<string:entity>', methods = ['GET','POST','PUT'])
def edituser(entity):
    form = BuatUser(request.form)
    form.userID.data = entity
    if request.method == 'POST':
        if form.validate() == False:
            flash('Isi seluruhnya')
            return render_template('formedit.html', form=form, entity=entity)
        else:
            requests.put('http://10.10.6.251:5000/api/v0.1/auth/caps',
                params={"entity":form.userID.data, "caps":[
                PilihCapsMon(form.MONr.data,form.MONw.data,form.MONx.data),
                PilihCapsOsd(form.OSDr.data,form.OSDw.data,form.OSDx.data),
                PilihCapsMds(form.MDSr.data,form.MDSw.data,form.MDSx.data)]},headers=headers)
            return redirect('/AddUser')
    elif request.method == 'GET':
        return render_template('formedit.html', form=form, entity=entity)

@app.route('/VolumeList',methods = ['GET','POST'])
def addvolume():
    req = requests.get('http://10.10.6.251:5000/api/v0.1/osd/pool/ls.json',headers=headers)
    pools = json.loads(req.text)
    r = requests.get('http://10.10.6.251:5000/api/v0.1/osd/pool/stats', params=pools.output,headers=headers)
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

@app.route('/latihanjson')
def latihanjson():
    req = requests.get('http://10.10.6.251:5000/api/v0.1/osd/pool/ls.json',headers=headers)
    ketext = json.loads(req.text)

    return render_template('parsing_json.html', pools=ketext)

if __name__=='__main__':
    app.run(host='0.0.0.0',port=8000,debug=True)
