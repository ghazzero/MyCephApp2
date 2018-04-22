from flask import Flask, request, render_template, flash, redirect
import requests
import json
from flask_wtf import Form
from wtforms import validators,StringField, IntegerField,SubmitField, BooleanField
from flask_cors import CORS
from blockdevice import PilihCapsMon, PilihCapsOsd, PilihCapsMds
#from blockdevice import newImage, newPool, list_image


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

class BuatPool(Form):
    namaPool = StringField('Nama Pool')
    PGnum = IntegerField('PG Number')
    PGPnum = IntegerField('PGP Number')
    submit = SubmitField()

class BuatImage(Form):
    namaPool = StringField('Nama Pool')
    namaImage = StringField('Nama Image')
    kapasitas = IntegerField('Kapasitas dalam GB')
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
def volumelist():
    r = requests.get('http://10.10.6.251:5000/api/v0.1/osd/pool/stats.json',headers=headers)
    images = []
    for data in json.loads(r.text)["output"]["pool_name"]:
        images.append(list_image(data))
    print images
    return render_template('addvolume.html', data=json.loads(r.text),images=images)

@app.route('/VolumeList/formpool', methods = ['GET','POST','PUT'])
def formpool():
    form = BuatPool(request.form)
    if request.method == 'POST':
	if form.validate() == False:
	return render_template('formpool.html', form=form)
        else: 
	  request.put('http://10.10.6.251:5000/api/v0.1/osd/pool/create',headers=headers, params = {'pool':form.namaPool.data, 'pg_num':form.pgnum.data, 'pgp_num':form.pgpnum.data)
	  return redirect('/VolumeList')
    if request.method == 'GET' 
    return render_template('formpool.html', form=form)	

@app.route('/VolumeList/formimage', methods = ['GET','POST','PUT'])
def formpool():
    form = BuatImage(request.form)
    if request.method == 'POST':
	if form.validate() == False:
	return render_template('formimage.html' form=form)
        else:
	   newImage(form.namaPool.data, form.namaImage.data, form.kapasitas.data)
	   return redirect('/VolumeList')
    if request.method == 'GET' 
return render_template('formimage.html' form=form) 						    

@app.route('/LinkUserVolume')
def linkuservolume():
    return render_template('home.html')

@app.route('/latihanjson')
def latihanjson():
    req = requests.get('http://10.10.6.251:5000/api/v0.1/osd/pool/stats.json',headers=headers)
    ketext = json.loads(req.text)
    return render_template('parsing_json.html', pools=ketext)

if __name__=='__main__':
    app.run(host='0.0.0.0',port=8000,debug=True)
