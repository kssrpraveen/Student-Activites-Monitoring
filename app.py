from werkzeug.wrappers import Request,Response
from flask import Flask,render_template,request,send_file,session,flash
import os
from io import BytesIO
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from base64 import b64encode,b64decode
from jinja2 import Environment
import pandas as pd
jinga_env=Environment(extensions=['jinja2.ext.loopcontrols'])
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
engine = create_engine("postgresql://postgres:kssr@localhost:5432/postgres")
db = scoped_session(sessionmaker(bind=engine))
app=Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')


@app.route("/")
def index():
    CNFM=""
    if not session.get('logged_in'):
        return render_template('logins.html',CNFM=CNFM)
    else:
        return render_template("bootlogout.html",CNFM=CNFM)


@app.route("/home")
def home():
    CNFM=""
    if not session.get('logged_in'):
        return render_template('logins.html',CNFM=CNFM)
    else:
        session.pop('activityname',None)
        return render_template("bootlogout.html",CNFM=CNFM)
@app.route("/codhome")
def codhome():
    CNFM=""
    if not session.get('logged_in'):
        return render_template('logins.html',CNFM=CNFM)
    else:
        session.pop('activityname',None)
        session.pop('info',None)
        return render_template("culturalcord.html",CNFM=CNFM)
@app.route("/whome")
def whome():
    CNFM=""
    if not session.get('logged_in'):
        return render_template('logins.html',CNFM=CNFM)
    else:
        return workingview()
@app.route("/dhome")
def dhome():
    CNFM=""
    if not session.get('logged_in'):
        return render_template('logins.html',CNFM=CNFM)
    else:
        return cse()
@app.route("/cse")
def cse():
    CNFM=""
    if not session.get('logged_in'):
        return render_template('logins.html',CNFM=CNFM)
    else:
        dataa=db.execute("SELECT username,socialhours,technical from login WHERE branch=:branch",{"branch":'CSE'})
        return render_template("dean.html",dataa=dataa,name='CSE')
@app.route("/ece")
def ece():
    CNFM=""
    if not session.get('logged_in'):
        return render_template('logins.html',CNFM=CNFM)
    else:
        dataa=db.execute("SELECT username,socialhours,technical from login WHERE branch=:branch",{"branch":'ECE'})
        return render_template("dean.html",dataa=dataa,name='ECE')
@app.route("/it")
def it():
    CNFM=""
    if not session.get('logged_in'):
        return render_template('logins.html',CNFM=CNFM)
    else:
        dataa=db.execute("SELECT username,socialhours,technical from login WHERE branch=:branch",{"branch":'IT'})
        return render_template("dean.html",dataa=dataa,name="IT")
@app.route("/mech")
def mech():
    CNFM=""
    if not session.get('logged_in'):
        return render_template('logins.html',CNFM=CNFM)
    else:
        dataa=db.execute("SELECT username,socialhours,technical from login WHERE branch=:branch",{"branch":'MECH'})
        return render_template("dean.html",dataa=dataa,name="MECH")
@app.route("/login", methods=['GET', 'POST'])
def login():
    POST_USERNAME = str(request.form.get("name")).strip()
    POST_PASSWORD = str(request.form.get("pass")).strip()
    if db.execute("SELECT * from login WHERE username= :username and password= :password",{"username": POST_USERNAME,"password": POST_PASSWORD}).rowcount == 1:
        if(len(POST_USERNAME)==10):
            session['logged_in'] = True
            session['username']=POST_USERNAME
            rdata=db.execute("SELECT reg,branch from login WHERE username= :username",{"username": POST_USERNAME})
            for i in rdata:
                session['reg']=i.reg
                session['branch']=i.branch
            
            return home()
        elif db.execute("SELECT * from login WHERE username= :username and level= :level",{"username":POST_USERNAME,"level": 1}).rowcount==1:
            session['logged_in'] = True
            session['username']=POST_USERNAME
            return codhome()
        elif db.execute("SELECT level from login WHERE username= :username and level= :level",{"username":POST_USERNAME,"level": 2}).rowcount==1:
            session['logged_in'] = True
            session['username']=POST_USERNAME
            CNFM=""
            return workingview()
        elif db.execute("SELECT level from login WHERE  username= :username and level= :level",{"username":POST_USERNAME,"level": 3}).rowcount==1:
            session['logged_in'] = True
            session['username']=POST_USERNAME
            CNFM=""
            return cse()
        else:
            return index()
            
    else:
        flash('wrong password!')
    return index()



def workingview():
    if session['username']=='cse@gvpce.ac.in':
        s=db.execute("SELECT username,sem1,sem2,sem3,sem4,sem5,sem6,sem7,sem8 FROM login WHERE branch=:branch",{"branch":'CSE'}).fetchall()
        dataa=sorted(s,key=lambda x:x[1])
        return render_template("working.html",dataa=dataa)
    elif session['username']=='ece@gvpce.ac.in':
        s=db.execute("SELECT username,sem1,sem2,sem3,sem4,sem5,sem6,sem7,sem8 FROM login WHERE branch=:branch",{"branch":'ECE'}).fetchall()
        dataa=sorted(s,key=lambda x:x[1])
        return render_template("working.html",dataa=dataa)
    elif session['username']=='it@gvpce.ac.in':
        s=db.execute("SELECT username,sem1,sem2,sem3,sem4,sem5,sem6,sem7,sem8 FROM login WHERE branch=:branch",{"branch":'IT'}).fetchall()
        dataa=sorted(s,key=lambda x:x[1])
        return render_template("working.html",dataa=dataa)
    elif session['username']=='mech@gvpce.ac.in':
        s=db.execute("SELECT username,sem1,sem2,sem3,sem4,sem5,sem6,sem7,sem8 FROM login WHERE branch=:branch",{"branch":'MECH'}).fetchall()
        dataa=sorted(s,key=lambda x:x[1])
        return render_template("working.html",dataa=dataa)


@app.route("/logout",methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    session.pop('username', None)
    session.pop('reg',None)
    session.pop('branch',None)
    return index()






@app.route("/searches", methods=['GET', 'POST'])
def searches():
    if session['username']=='culturals@gvpce.ac.in':
        rno=str(request.form.get("sroll")).strip()
        #dataa=db.execute("SELECT encode(places.img::bytea, 'base64'),infors.rollno,infors.activityname,infors.activitydesc,infors.fromdate,infors.todate,infors.wdays,infors.lopartic,infors.popartic from places,infors where places.id=infors.id and infors.rollno=:rollno",{"rollno":rno}).fetchall()
        dataa=db.execute("SELECT encode(img::bytea, 'base64'),id,rollno,reg,branch,year,semester,activityname,activitydesc,fromdate,todate,wdays,lopartic,popartic,status from cultural where rollno=:rollno",{"rollno":rno}).fetchall()
        #s=pd.DataFrame(dataa,columns=['image','id','rollno','activityname','activitydesc','fromdate','todate','lopartic','wdays','popartic','status'])
        data=dataa[0]
        if data[14]=='yes':
            name=session['username']
            session['activityname']='cultural'
            return render_template("apdisplay.html",dataa=dataa,name=name) 
        else:
            name=session['username']
            session['activityname']='cultural'
            return render_template("display.html",dataa=dataa,name=name)
    elif session['username']=='literacy@gvpce.ac.in':
        rno=str(request.form.get("sroll")).strip()
        #dataa=db.execute("SELECT encode(places.img::bytea, 'base64'),infors.rollno,infors.activityname,infors.activitydesc,infors.fromdate,infors.todate,infors.wdays,infors.lopartic,infors.popartic from places,infors where places.id=infors.id and infors.rollno=:rollno",{"rollno":rno}).fetchall()
        dataa=db.execute("SELECT encode(img::bytea, 'base64'),id,rollno,reg,branch,year,semester,activityname,activitydesc,fromdate,todate,wdays,lopartic,popartic,status from literacy where rollno=:rollno",{"rollno":rno}).fetchall()
        #s=pd.DataFrame(dataa,columns=['image','id','rollno','activityname','activitydesc','fromdate','todate','lopartic','wdays','popartic','status'])
        #print(s)
        data=dataa[0]
        if data[14]=='yes':
            name=session['username']
            session['activityname']='literacy'
            return render_template("apdisplay.html",dataa=dataa,name=name)
        else:
            name=session['username']
            session['activityname']='literacy'
            return render_template("display.html",dataa=dataa,name=name)
    elif session['username']=='sports@gvpce.ac.in':
        rno=str(request.form.get("sroll")).strip()
        #dataa=db.execute("SELECT encode(places.img::bytea, 'base64'),infors.rollno,infors.activityname,infors.activitydesc,infors.fromdate,infors.todate,infors.wdays,infors.lopartic,infors.popartic from places,infors where places.id=infors.id and infors.rollno=:rollno",{"rollno":rno}).fetchall()
        dataa=db.execute("SELECT encode(img::bytea, 'base64'),id,rollno,reg,year,semester,branch,activityname,activitydesc,fromdate,todate,wdays,lopartic,popartic,status from sport where rollno=:rollno",{"rollno":rno}).fetchall()
        #s=pd.DataFrame(dataa,columns=['image','id','rollno','activityname','activitydesc','fromdate','todate','lopartic','wdays','popartic','status'])
        #print(s)
        data=dataa[0]
        if data[14]=='yes':
            name=session['username']
            session['activityname']='sports'
            return render_template("apdisplay.html",dataa=dataa,name=name)
        else:
            name=session['username']
            session['activityname']='sports'
            return render_template("display.html",dataa=dataa,name=name)
    elif session['username']=='seminar@gvpce.ac.in':
        rno=str(request.form.get("sroll")).strip()
        #dataa=db.execute("SELECT encode(places.img::bytea, 'base64'),infors.rollno,infors.activityname,infors.activitydesc,infors.fromdate,infors.todate,infors.wdays,infors.lopartic,infors.popartic from places,infors where places.id=infors.id and infors.rollno=:rollno",{"rollno":rno}).fetchall()
        dataa=db.execute("SELECT encode(img::bytea, 'base64'),id,rollno,reg,year,semester,branch,activityname,activitydesc,fromdate,todate,wdays,lopartic,popartic,status from seminar where rollno=:rollno",{"rollno":rno}).fetchall()
        #s=pd.DataFrame(dataa,columns=['image','id','rollno','activityname','activitydesc','fromdate','todate','lopartic','wdays','popartic','status'])
        #print(s)
        data=dataa[0]
        if data[14]=='yes':
            name=session['username']
            session['activityname']='seminar'
            return render_template("apdisplay.html",dataa=dataa,name=name)
        else:
            name=session['username']
            session['activityname']='seminar'
            return render_template("display.html",dataa=dataa,name=name)
    elif session['username']=='social@gvpce.ac.in':
        rno=str(request.form.get("sroll")).strip()
        #dataa=db.execute("SELECT encode(places.img::bytea, 'base64'),infors.rollno,infors.activityname,infors.activitydesc,infors.fromdate,infors.todate,infors.wdays,infors.lopartic,infors.popartic from places,infors where places.id=infors.id and infors.rollno=:rollno",{"rollno":rno}).fetchall()
        dataa=db.execute("SELECT encode(img::bytea, 'base64'),id,rollno,reg,year,semester,branch,activityname,activitydesc,fromdate,todate,wdays,lopartic,popartic,status from social where rollno=:rollno",{"rollno":rno}).fetchall()
        #s=pd.DataFrame(dataa,columns=['image','id','rollno','activityname','activitydesc','fromdate','todate','lopartic','wdays','popartic','status'])
        #print(s)
        data=dataa[0]
        if data[14]=='yes':
            name=session['username']
            session['activityname']='social'
            return render_template("apdisplay.html",dataa=dataa,name=name)
        else:
            name=session['username']
            session['activityname']='social'
            return render_template("display.html",dataa=dataa,name=name)
    elif session['username']=='nss@gvpce.ac.in':
        rno=str(request.form.get("sroll")).strip()
        #dataa=db.execute("SELECT encode(places.img::bytea, 'base64'),infors.rollno,infors.activityname,infors.activitydesc,infors.fromdate,infors.todate,infors.wdays,infors.lopartic,infors.popartic from places,infors where places.id=infors.id and infors.rollno=:rollno",{"rollno":rno}).fetchall()
        s=db.execute("SELECT encode(img::bytea, 'base64'),id,rollno,reg,year,semester,branch,activityname,activitydesc,fromdate,todate,wdays,lopartic,popartic,status from nss where rollno=:rollno",{"rollno":rno}).fetchall()
        #s=pd.DataFrame(dataa,columns=['image','id','rollno','activityname','activitydesc','fromdate','todate','lopartic','wdays','popartic','status'])
        #print(s)
        dataa=s[0]
        if dataa[14]=='yes':
            name=session['username']
            session['activityname']='nss'
            return render_template("apdisplay.html",dataa=dataa,name=name)
        else:
            name=session['username']
            session['activityname']='nss'
            return render_template("display.html",dataa=dataa,name=name)
    elif session['username']=='cse@gvpce.ac.in':
        rno=str(request.form.get("sroll")).strip()
        dataa=db.execute("SELECT username,sem1,sem2,sem3,sem4,sem5,sem6,sem7,sem8 FROM login WHERE branch=:branch and username=:username",{"branch":'CSE',"username":rno}).fetchall()
        return render_template("inddisplay.html",dataa=dataa,name=rno)
    elif session['username']=='ece@gvpce.ac.in':
        rno=str(request.form.get("sroll")).strip()
        dataa=db.execute("SELECT username,sem1,sem2,sem3,sem4,sem5,sem6,sem7,sem8 FROM login WHERE branch=:branch and username=:username",{"branch":'ECE',"username":rno}).fetchall()
        return render_template("inddisplay.html",dataa=dataa,name=rno)
    elif session['username']=='it@gvpce.ac.in':
        rno=str(request.form.get("sroll")).strip()
        dataa=db.execute("SELECT username,sem1,sem2,sem3,sem4,sem5,sem6,sem7,sem8 FROM login WHERE branch=:branch and username=:username",{"branch":'IT',"username":rno}).fetchall()
        return render_template("inddisplay.html",dataa=dataa,name=rno)
    elif session['username']=='mech@gvpce.ac.in':
        rno=str(request.form.get("sroll")).strip()
        dataa=db.execute("SELECT username,sem1,sem2,sem3,sem4,sem5,sem6,sem7,sem8 FROM login WHERE branch=:branch and username=:username",{"branch":'MECH',"username":rno}).fetchall()
        return render_template("inddisplay.html",dataa=dataa,name=rno)
    elif session['username']=="dean@gvpce.ac.in":
        rno=str(request.form.get("sroll")).strip()
        dataa=db.execute("SELECT username,branch,socialhours,technical FROM login WHERE username=:username",{"username":rno}).fetchall()
        return render_template("ddisplay.html",dataa=dataa)


    


@app.route("/editprofile/<int:id>",methods=['GET', 'POST'])
def editprofile(id):
    if not session.get('logged_in'):
        CNFM="please login"
        return render_template('logins.html',CNFM=CNFM)
    else:
    #id=request.form.get("id")
        if session['activityname']=='cultural':
            uudata=db.execute("SELECT id,rollno,reg,year,semester,branch,activityname,activitydesc,fromdate,todate,wdays,lopartic,popartic,status from cultural where id=:id",{"id":id}).fetchall()
            udata=uudata[0]
            session['id']=udata[0]
            session['activityname']=udata[6]
            return render_template("update.html",udata=udata)
        elif session['activityname']=='literacy':
            uudata=db.execute("SELECT id,rollno,reg,year,semester,branch,activityname,activitydesc,fromdate,todate,wdays,lopartic,popartic,status from literacy where id=:id",{"id":id}).fetchall()
            udata=uudata[0]
            session['id']=udata[0]
            session['activityname']=udata[6]
            return render_template("update.html",udata=udata)
        elif session['activityname']=='sports':
            uudata=db.execute("SELECT id,rollno,reg,year,semester,branch,activityname,activitydesc,fromdate,todate,wdays,lopartic,popartic,status from sport where id=:id",{"id":id}).fetchall()
            udata=uudata[0]
            session['id']=udata[0]
            session['activityname']=udata[6]
            return render_template("update.html",udata=udata)
        elif session['activityname']=='seminar':
            uudata=db.execute("SELECT id,rollno,reg,year,semester,branch,activityname,activitydesc,fromdate,todate,wdays,lopartic,popartic,status from seminar where id=:id",{"id":id}).fetchall()
            udata=uudata[0]
            session['id']=udata[0]
            session['activityname']=udata[6]
            return render_template("update.html",udata=udata)
        elif session['activityname']=='social':
            uudata=db.execute("SELECT id,rollno,reg,year,semester,branch,activityname,activitydesc,fromdate,todate,wdays,lopartic,popartic,status from social where id=:id",{"id":id}).fetchall()
            udata=uudata[0]
            session['id']=udata[0]
            session['activityname']=udata[6]
            return render_template("update.html",udata=udata)
        elif session['activityname']=='nss':
            uudata=db.execute("SELECT id,rollno,reg,year,semester,branch,activityname,activitydesc,fromdate,todate,wdays,lopartic,popartic,status from nss where id=:id",{"id":id}).fetchall()
            udata=uudata[0]
            session['id']=udata[0]
            session['activityname']=udata[6]
            return render_template("update.html",udata=udata)
        return render_template("bootlogout.html")
@app.route("/deleteprofile/<int:id>",methods=['GET', 'POST'])
def deleteprofile(id):
    if not session.get('logged_in'):
        CNFM="please login"
        return render_template('logins.html',CNFM=CNFM)
    else:
        if session['activityname']=='cultural':
            db.execute("DELETE from cultural WHERE id= :id",{"id":id})
            db.commit();
            return vcultural()
        elif session['activityname']=='literacy':
            db.execute("DELETE from literacy WHERE id= :id",{"id":id})
            db.commit();
            return vliteracy()
        elif session['activityname']=='sports':
            db.execute("DELETE from sport WHERE id= :id",{"id":id})
            db.commit();
            return vsports()
        elif session['activityname']=='seminar':
            db.execute("DELETE from seminar WHERE id= :id",{"id":id})
            db.commit();
            return vseminar()
        elif session['activityname']=='social':
            db.execute("DELETE from social WHERE id= :id",{"id":id})
            db.commit();
            return vsocial()
        elif session['activityname']=='nss':
            db.execute("DELETE from nss WHERE id= :id",{"id":id})
            db.commit();
            return vnss()
        return render_template("bootlogout.html")
@app.route('/updateevent',methods=['GET', 'POST'])
def updateevent():
    if not session.get('logged_in'):
        CNFM="please login"
        return render_template('logins.html',CNFM=CNFM)
    else:
        ids=session['id']
        activityname=session['activityname']
        years=int(request.form.get('yearp'))
        sem=int(request.form.get('sem'))
        activitydes=request.form.get('activityd')
        frdates=request.form.get('frdate')
        todates=request.form.get('todate')
        workings=request.form.get('working')
        levelps=request.form.get('levelp')
        placesps=request.form.get('placep')
        print(activityname)
        print(years)
        print(placesps)
        if activityname=="cultural":
            db.execute("UPDATE cultural SET year = :year,semester = :semester,activitydesc = :activitydesc,fromdate = :fromdate,todate = :todate,wdays =:wdays,lopartic =:lopartic,popartic =:popartic WHERE id=:id",{"year":years,"semester":sem,"activitydesc":activitydes,"fromdate":frdates,"todate":todates,"wdays":workings,"lopartic":levelps,"popartic":placesps,"id":ids})
            print("success")
            db.commit();
            session.pop('id',None)
            if len(session['username'])==10:
                return vcultural()
            else:
                if session['info']=='approved':
                    return approved()
                elif session['info']=='notapproved':
                    return notapproved()
        elif activityname=="literacy":
            db.execute("UPDATE literacy SET year = :year,semester = :semester,activitydesc = :activitydesc,fromdate = :fromdate,todate = :todate,wdays =:wdays,lopartic =:lopartic,popartic =:popartic WHERE id=:id",{"year":years,"semester":sem,"activitydesc":activitydes,"fromdate":frdates,"todate":todates,"wdays":workings,"lopartic":levelps,"popartic":placesps,"id":ids})
            print("success")
            db.commit();
            session.pop('id',None)
            if len(session['username'])==10:
                return vliteracy()
            else:
                if session['info']=='approved':
                    return approved()
                elif session['info']=='notapproved':
                    return notapproved()
        elif activityname=="sports":
            db.execute("UPDATE sport SET year = :year,semester = :semester,activitydesc = :activitydesc,fromdate = :fromdate,todate = :todate,wdays =:wdays,lopartic =:lopartic,popartic =:popartic WHERE id=:id",{"year":years,"semester":sem,"activitydesc":activitydes,"fromdate":frdates,"todate":todates,"wdays":workings,"lopartic":levelps,"popartic":placesps,"id":ids})
            print("success")
            db.commit();
            session.pop('id',None)
            if len(session['username'])==10:
                return vsports()
            else:
                if session['info']=='approved':
                    return approved()
                elif session['info']=='notapproved':
                    return notapproved()
        elif activityname=="seminar":
            db.execute("UPDATE seminar SET year = :year,semester = :semester,activitydesc = :activitydesc,fromdate = :fromdate,todate = :todate,wdays =:wdays,lopartic =:lopartic,popartic =:popartic WHERE id=:id",{"year":years,"semester":sem,"activitydesc":activitydes,"fromdate":frdates,"todate":todates,"wdays":workings,"lopartic":levelps,"popartic":placesps,"id":ids})
            print("success")
            db.commit();
            session.pop('id',None)
            if len(session['username'])==10:
                return vseminar()
            else:
                if session['info']=='approved':
                    return approved()
                elif session['info']=='notapproved':
                    return notapproved()
        elif activityname=="social":
            db.execute("UPDATE social SET year = :year,semester = :semester,activitydesc = :activitydesc,fromdate = :fromdate,todate = :todate,wdays =:wdays,lopartic =:lopartic,popartic =:popartic WHERE id=:id",{"year":years,"semester":sem,"activitydesc":activitydes,"fromdate":frdates,"todate":todates,"wdays":workings,"lopartic":levelps,"popartic":placesps,"id":ids})
            print("success")
            db.commit();
            session.pop('id',None)
            if len(session['username'])==10:
                return vsocial()
            else:
                if session['info']=='approved':
                    return approved()
                elif session['info']=='notapproved':
                    return notapproved()
        elif activityname=="nss":
            db.execute("UPDATE nss SET year = :year,semester = :semester,activitydesc = :activitydesc,fromdate = :fromdate,todate = :todate,wdays =:wdays,lopartic =:lopartic,popartic =:popartic WHERE id=:id",{"year":years,"semester":sem,"activitydesc":activitydes,"fromdate":frdates,"todate":todates,"wdays":workings,"lopartic":levelps,"popartic":placesps,"id":ids})
            print("success")
            db.commit();
            session.pop('id',None)
            if len(session['username'])==10:
                return vnss()
            else:
                if session['info']=='approved':
                    return approved()
                elif session['info']=='notapproved':
                    return notapproved()
        sn="its not a cultural database"
        return render_template("infos.html",sn=sn)
    
@app.route("/cultural", methods=['GET', 'POST'])
def cultural():
    if not session.get('logged_in'):
        CNFM="please login"
        return render_template('logins.html',CNFM=CNFM)
    else:
        session['activityname']="cultural"
        return render_template("register.html")
@app.route("/vcultural", methods=['GET', 'POST'])
def vcultural():
    if not session.get('logged_in'):
        CNFM="please login"
        return render_template('logins.html',CNFM=CNFM)
    else:
        rno=session['username']
        s=db.execute("SELECT encode(img::bytea, 'base64'),id,rollno,reg,year,semester,branch,activityname,activitydesc,fromdate,todate,wdays,lopartic,popartic,status from cultural where rollno=:rollno",{"rollno":rno}).fetchall()
        dataa=sorted(s,key=lambda x:x[13],reverse=True)
        session['activityname']="cultural"
        name=session['activityname']
        return render_template("searchresult.html",dataa=dataa,name=name)  
@app.route("/literacy", methods=['GET', 'POST'])
def literacy():
    if not session.get('logged_in'):
        CNFM="please login"
        return render_template('logins.html',CNFM=CNFM)
    else:
        session['activityname']="literacy"
        return render_template("register.html")
@app.route("/vliteracy", methods=['GET', 'POST'])
def vliteracy():
    if not session.get('logged_in'):
        CNFM="please login"
        return render_template('logins.html',CNFM=CNFM)
    else:
        rno=session['username']
        s=db.execute("SELECT encode(img::bytea, 'base64'),id,rollno,reg,year,semester,branch,activityname,activitydesc,fromdate,todate,wdays,lopartic,popartic,status from literacy where rollno=:rollno",{"rollno":rno}).fetchall()
        dataa=sorted(s,key=lambda x:x[13],reverse=True)
        session['activityname']="literacy"
        name=session['activityname']
        return render_template("searchresult.html",dataa=dataa,name=name)  
@app.route("/sports", methods=['GET', 'POST'])
def sports():
    if not session.get('logged_in'):
        CNFM="please login"
        return render_template('logins.html',CNFM=CNFM)
    else:
        session['activityname']="sports"
        return render_template("register.html")
@app.route("/vsports", methods=['GET', 'POST'])
def vsports():
    if not session.get('logged_in'):
        CNFM="please login"
        return render_template('logins.html',CNFM=CNFM)
    else:
        rno=session['username']
        s=db.execute("SELECT encode(img::bytea, 'base64'),id,rollno,reg,year,semester,branch,activityname,activitydesc,fromdate,todate,wdays,lopartic,popartic,status from sport where rollno=:rollno",{"rollno":rno}).fetchall()
        dataa=sorted(s,key=lambda x:x[13],reverse=True)
        session['activityname']="sports"
        name=session['activityname']
        return render_template("searchresult.html",dataa=dataa,name=name)  
@app.route("/seminar", methods=['GET', 'POST'])
def seminar():
    if not session.get('logged_in'):
        CNFM="please login"
        return render_template('logins.html',CNFM=CNFM)
    else:
        session['activityname']="seminar"
        return render_template("register.html")
@app.route("/vseminar", methods=['GET', 'POST'])
def vseminar():
    if not session.get('logged_in'):
        CNFM="please login"
        return render_template('logins.html',CNFM=CNFM)
    else:
        rno=session['username']
        s=db.execute("SELECT encode(img::bytea, 'base64'),id,rollno,reg,year,semester,branch,activityname,activitydesc,fromdate,todate,wdays,lopartic,popartic,status from seminar where rollno=:rollno",{"rollno":rno}).fetchall()
        dataa=sorted(s,key=lambda x:x[13],reverse=True)
        session['activityname']="seminar"
        name=session['activityname']
        return render_template("searchresult.html",dataa=dataa,name=name) 
@app.route("/social", methods=['GET', 'POST'])
def social():
    if not session.get('logged_in'):
        CNFM="please login"
        return render_template('logins.html',CNFM=CNFM)
    else:
        session['activityname']="social"
        return render_template("register.html")
@app.route("/vsocial", methods=['GET', 'POST'])
def vsocial():
    if not session.get('logged_in'):
        CNFM="please login"
        return render_template('logins.html',CNFM=CNFM)
    else:
        rno=session['username']
        s=db.execute("SELECT encode(img::bytea, 'base64'),id,rollno,reg,year,semester,branch,activityname,activitydesc,fromdate,todate,wdays,lopartic,popartic,status from social where rollno=:rollno",{"rollno":rno}).fetchall()
        dataa=sorted(s,key=lambda x:x[13],reverse=True)
        session['activityname']="social"
        name=session['activityname']
        return render_template("searchresult.html",dataa=dataa,name=name) 
@app.route("/nss", methods=['GET', 'POST'])
def nss():
    if not session.get('logged_in'):
        CNFM="please login"
        return render_template('logins.html',CNFM=CNFM)
    else:
        session['activityname']="nss"
        return render_template("register.html")
@app.route("/vnss", methods=['GET', 'POST'])
def vnss():
    if not session.get('logged_in'):
        CNFM="please login"
        return render_template('logins.html',CNFM=CNFM)
    else:
        rno=session['username']
        s=db.execute("SELECT encode(img::bytea, 'base64'),id,rollno,reg,year,semester,branch,activityname,activitydesc,fromdate,todate,wdays,lopartic,popartic,status from nss where rollno=:rollno",{"rollno":rno}).fetchall()
        dataa=sorted(s,key=lambda x:x[12],reverse=True)
        session['activityname']="nss"
        name=session['activityname']
        return render_template("searchresult.html",dataa=dataa,name=name) 
@app.route("/notapproved", methods=['GET', 'POST'])
def notapproved():
    if not session.get('logged_in'):
        CNFM="please login"
        return render_template('logins.html',CNFM=CNFM)
    else:
        session['info']="notapproved"
        if session['username']=="culturals@gvpce.ac.in":
            dataa=db.execute("SELECT encode(img::bytea, 'base64'),id,rollno,reg,year,semester,branch,activityname,activitydesc,fromdate,todate,wdays,lopartic,popartic,status from cultural where status=:status",{"status":'no'}).fetchall()
            name=session['username']
            session['activityname']='cultural'
            return render_template("display.html",dataa=dataa,name=name)
        elif session['username']=="literacy@gvpce.ac.in":
            dataa=db.execute("SELECT encode(img::bytea, 'base64'),id,rollno,reg,year,semester,branch,activityname,activitydesc,fromdate,todate,wdays,lopartic,popartic,status from literacy where status=:status",{"status":'no'}).fetchall()
            name=session['username']
            session['activityname']='literacy'
            return render_template("display.html",dataa=dataa,name=name)
        elif session['username']=="sports@gvpce.ac.in":
            dataa=db.execute("SELECT encode(img::bytea, 'base64'),id,rollno,reg,year,semester,branch,activityname,activitydesc,fromdate,todate,wdays,lopartic,popartic,status from sport where status=:status",{"status":'no'}).fetchall()
            name=session['username']
            session['activityname']='sports'
            return render_template("display.html",dataa=dataa,name=name)   
        elif session['username']=="seminar@gvpce.ac.in":
            dataa=db.execute("SELECT encode(img::bytea, 'base64'),id,rollno,reg,year,semester,branch,activityname,activitydesc,fromdate,todate,wdays,lopartic,popartic,status from seminar where status=:status",{"status":'no'}).fetchall()
            name=session['username']
            session['activityname']='seminar'
            return render_template("display.html",dataa=dataa,name=name) 
        elif session['username']=="social@gvpce.ac.in":
            dataa=db.execute("SELECT encode(img::bytea, 'base64'),id,rollno,reg,year,branch,activityname,activitydesc,fromdate,todate,wdays,lopartic,popartic,status from social where status=:status",{"status":'no'}).fetchall()
            name=session['username']
            session['activityname']='social'
            return render_template("display.html",dataa=dataa,name=name) 
        elif session['username']=="nss@gvpce.ac.in":
            dataa=db.execute("SELECT encode(img::bytea, 'base64'),id,rollno,reg,year,semester,branch,activityname,activitydesc,fromdate,todate,wdays,lopartic,popartic,status from nss where status=:status",{"status":'no'}).fetchall()
            name=session['username']
            session['activityname']='nss'
            return render_template("display.html",dataa=dataa,name=name) 
@app.route("/approved", methods=['GET', 'POST'])
def approved():
    if not session.get('logged_in'):
        CNFM="please login"
        return render_template('logins.html',CNFM=CNFM)
    else:
        session['info']="approved"
        if session['username']=="culturals@gvpce.ac.in":
            dataa=db.execute("SELECT encode(img::bytea, 'base64'),id,rollno,reg,year,semester,branch,activityname,activitydesc,fromdate,todate,wdays,lopartic,popartic,status from cultural where status=:status",{"status":'yes'}).fetchall()
            name=session['username']
            session['activityname']='cultural'
            return render_template("apdisplay.html",dataa=dataa,name=name)  
        elif session['username']=="literacy@gvpce.ac.in":
            dataa=db.execute("SELECT encode(img::bytea, 'base64'),id,rollno,reg,year,semester,branch,activityname,activitydesc,fromdate,todate,wdays,lopartic,popartic,status from literacy where status=:status",{"status":'yes'}).fetchall()
            name=session['username']
            session['activityname']='literacy'
            return render_template("apdisplay.html",dataa=dataa,name=name)
        elif session['username']=="sports@gvpce.ac.in":
            dataa=db.execute("SELECT encode(img::bytea, 'base64'),id,rollno,reg,year,semester,branch,activityname,activitydesc,fromdate,todate,wdays,lopartic,popartic,status from sport where status=:status",{"status":'yes'}).fetchall()
            name=session['username']
            session['activityname']='sports'
            return render_template("apdisplay.html",dataa=dataa,name=name)  
        elif session['username']=="seminar@gvpce.ac.in":
            dataa=db.execute("SELECT encode(img::bytea, 'base64'),id,rollno,reg,year,semester,branch,activityname,activitydesc,fromdate,todate,wdays,lopartic,popartic,status from seminar where status=:status",{"status":'yes'}).fetchall()
            name=session['username']
            session['activityname']='seminar'
            return render_template("apdisplay.html",dataa=dataa,name=name) 
        elif session['username']=="social@gvpce.ac.in":
            dataa=db.execute("SELECT encode(img::bytea, 'base64'),id,rollno,reg,year,semester,branch,activityname,activitydesc,fromdate,todate,wdays,lopartic,popartic,status from social where status=:status",{"status":'yes'}).fetchall()
            name=session['username']
            session['activityname']='social'
            return render_template("apdisplay.html",dataa=dataa,name=name) 
        elif session['username']=="nss@gvpce.ac.in":
            dataa=db.execute("SELECT encode(img::bytea, 'base64'),id,rollno,reg,year,semester,branch,activityname,activitydesc,fromdate,todate,wdays,lopartic,popartic,status from nss where status=:status",{"status":'yes'}).fetchall()
            name=session['username']
            session['activityname']='nss'
            return render_template("apdisplay.html",dataa=dataa,name=name) 
def updateworking(ll):
    for k in ll:
        if k[1]==1: 
            #s=db.execute("SELECT rollno,semester,wdays,lopartic,activityname from cultural WHERE id=:id",{"id":id}
            da=db.execute("SELECT sem1,socialhours,technical from login WHERE username=:username",{"username":k[0]})
            for i in da:
                po=i[0]+k[2]
                if k[4]=='cultural' or k[4]=='social' or k[4]=='nss' or k[4]=='sports':
                    if k[3]=='our college':
                        work=(k[2]*3)+i[1]
                    else:
                         work=(k[2]*5)+i[1]
                    db.execute("UPDATE login SET sem1=:sem1,socialhours=:socialhours WHERE username=:username",{"sem1":po,"socialhours":work,"username":k[0]})
                    db.commit()
                elif k[4]=='literacy' or k[4]=='seminar':
                    if k[3]=='our college':
                        work=(k[2]*3)+i[2]
                    else:
                        work=(k[2]*5)+i[2]
                    db.execute("UPDATE login SET sem1=:sem1,technical=:technical WHERE username=:username",{"sem1":po,"technical":work,"username":k[0]})
                    db.commit()

        elif k[1]==2:
            da=db.execute("SELECT sem2,socialhours,technical from login WHERE username=:username",{"username":k[0]})
            for i in da:
                po=i[0]+k[2]
                if k[4]=='cultural' or k[4]=='social' or k[4]=='nss' or k[4]=='sports':
                    if k[3]=='our college':
                        work=(k[2]*3)+i[1]
                    else:
                         work=(k[2]*5)+i[1]
                    db.execute("UPDATE login SET sem2=:sem2,socialhours=:socialhours WHERE username=:username",{"sem2":po,"socialhours":work,"username":k[0]})
                    db.commit()
                elif k[4]=='literacy' or k[4]=='seminar':
                    if k[3]=='our college':
                        work=(k[2]*3)+i[2]
                    else:
                        work=(k[2]*5)+i[2]
                    db.execute("UPDATE login SET sem2=:sem2,technical=:technical WHERE username=:username",{"sem2":po,"technical":work,"username":k[0]})
                    db.commit()
        elif k[1]==3:
            da=db.execute("SELECT sem3,socialhours,technical from login WHERE username=:username",{"username":k[0]})
            for i in da:
                po=i[0]+k[2]
                if k[4]=='cultural' or k[4]=='social' or k[4]=='nss' or k[4]=='sports':
                    if k[3]=='our college':
                        work=(k[2]*3)+i[1]
                    else:
                         work=(k[2]*5)+i[1]
                    db.execute("UPDATE login SET sem3=:sem3,socialhours=:socialhours WHERE username=:username",{"sem3":po,"socialhours":work,"username":k[0]})
                    db.commit()
                elif k[4]=='literacy' or k[4]=='seminar':
                    if k[3]=='our college':
                        work=(k[2]*3)+i[2]
                    else:
                        work=(k[2]*5)+i[2]
                    db.execute("UPDATE login SET sem3=:sem3,technical=:technical WHERE username=:username",{"sem3":po,"technical":work,"username":k[0]})
                    db.commit()
        elif k[1]==4:
            da=db.execute("SELECT sem4,socialhours,technical from login WHERE username=:username",{"username":k[0]})
            for i in da:
                po=i[0]+k[2]
                if k[4]=='cultural' or k[4]=='social' or k[4]=='nss' or k[4]=='sports':
                    if k[3]=='our college':
                        work=(k[2]*3)+i[1]
                    else:
                         work=(k[2]*5)+i[1]
                    db.execute("UPDATE login SET sem4=:sem4,socialhours=:socialhours WHERE username=:username",{"sem4":po,"socialhours":work,"username":k[0]})
                    db.commit()
                elif k[4]=='literacy' or k[4]=='seminar':
                    if k[3]=='our college':
                        work=(k[2]*3)+i[2]
                    else:
                        work=(k[2]*5)+i[2]
                    db.execute("UPDATE login SET sem4=:sem4,technical=:technical WHERE username=:username",{"sem4":po,"technical":work,"username":k[0]})
                    db.commit()
        elif k[1]==5:
            da=db.execute("SELECT sem5,socialhours,technical from login WHERE username=:username",{"username":k[0]})
            for i in da:
                po=i[0]+k[2]
                if k[4]=='cultural' or k[4]=='social' or k[4]=='nss' or k[4]=='sports':
                    if k[3]=='our college':
                        work=(k[2]*3)+i[1]
                    else:
                         work=(k[2]*5)+i[1]
                    db.execute("UPDATE login SET sem5=:sem5,socialhours=:socialhours WHERE username=:username",{"sem5":po,"socialhours":work,"username":k[0]})
                    db.commit()
                elif k[4]=='literacy' or k[4]=='seminar':
                    if k[3]=='our college':
                        work=(k[2]*3)+i[2]
                    else:
                        work=(k[2]*5)+i[2]
                    db.execute("UPDATE login SET sem5=:sem5,technical=:technical WHERE username=:username",{"sem5":po,"technical":work,"username":k[0]})
                    db.commit()
        elif k[1]==6:
            da=db.execute("SELECT sem6,socialhours,technical from login WHERE username=:username",{"username":k[0]})
            for i in da:
                po=i[0]+k[2]
                if k[4]=='cultural' or k[4]=='social' or k[4]=='nss' or k[4]=='sports':
                    if k[3]=='our college':
                        work=(k[2]*3)+i[1]
                    else:
                         work=(k[2]*5)+i[1]
                    db.execute("UPDATE login SET sem6=:sem6,socialhours=:socialhours WHERE username=:username",{"sem6":po,"socialhours":work,"username":k[0]})
                    db.commit()
                elif k[4]=='literacy' or k[4]=='seminar':
                    if k[3]=='our college':
                        work=(k[2]*3)+i[2]
                    else:
                        work=(k[2]*5)+i[2]
                    db.execute("UPDATE login SET sem6=:sem6,technical=:technical WHERE username=:username",{"sem6":po,"technical":work,"username":k[0]})
                    db.commit()
        elif k[1]==7:
            da=db.execute("SELECT sem7,socialhours,technical from login WHERE username=:username",{"username":k[0]})
            for i in da:
                po=i[0]+k[2]
                if k[4]=='cultural' or k[4]=='social' or k[4]=='nss' or k[4]=='sports':
                    if k[3]=='our college':
                        work=(k[2]*3)+i[1]
                    else:
                         work=(k[2]*5)+i[1]
                    db.execute("UPDATE login SET sem7=:sem7,socialhours=:socialhours WHERE username=:username",{"sem7":po,"socialhours":work,"username":k[0]})
                    db.commit()
                elif k[4]=='literacy' or k[4]=='seminar':
                    if k[3]=='our college':
                        work=(k[2]*3)+i[2]
                    else:
                        work=(k[2]*5)+i[2]
                    db.execute("UPDATE login SET sem7=:sem7,technical=:technical WHERE username=:username",{"sem7":po,"technical":work,"username":k[0]})
                    db.commit()
        elif k[1]==8:
            da=db.execute("SELECT sem8,socialhours,technical from login WHERE username=:username",{"username":k[0]})
            for i in da:
                po=i[0]+k[2]
                if k[4]=='cultural' or k[4]=='social' or k[4]=='nss' or k[4]=='sports':
                    if k[3]=='our college':
                        work=(k[2]*3)+i[1]
                    else:
                         work=(k[2]*5)+i[1]
                    db.execute("UPDATE login SET sem8=:sem8,socialhours=:socialhours WHERE username=:username",{"sem8":po,"socialhours":work,"username":k[0]})
                    db.commit()
                elif k[4]=='literacy' or k[4]=='seminar':
                    if k[3]=='our college':
                        work=(k[2]*3)+i[2]
                    else:
                        work=(k[2]*5)+i[2]
                    db.execute("UPDATE login SET sem8=:sem8,technical=:technical WHERE username=:username",{"sem8":po,"technical":work,"username":k[0]})
                    db.commit()


@app.route("/aprooveprofile/<int:id>",methods=['GET', 'POST'])
def aprooveprofile(id):
    if not session.get('logged_in'):
        CNFM="please login"
        return render_template('logins.html',CNFM=CNFM)
    else:
        if session['activityname']=='cultural':
            db.execute("UPDATE cultural SET status= :status WHERE id=:id",{"status":"yes","id":id})
            print("success")
            db.commit();
            ll=db.execute("SELECT rollno,semester,wdays,lopartic,activityname from cultural WHERE id=:id",{"id":id})
            updateworking(ll)
            session.pop('id',None)
            if session['info']=='approved':
                return approved()
            elif session['info']=='notapproved':
                return notapproved()
        elif session['activityname']=='literacy':
            db.execute("UPDATE literacy SET status= :status WHERE id=:id",{"status":"yes","id":id})
            print("success")
            db.commit();
            ll=db.execute("SELECT rollno,semester,wdays,lopartic,activityname from literacy WHERE id=:id",{"id":id})
            updateworking(ll)
            session.pop('id',None)
            if session['info']=='approved':
                return approved()
            elif session['info']=='notapproved':
                return notapproved()
        elif session['activityname']=='sports':
            db.execute("UPDATE sport SET status= :status WHERE id=:id",{"status":"yes","id":id})
            print("success")
            db.commit();
            ll=db.execute("SELECT rollno,semester,wdays,lopartic,activityname from sport WHERE id=:id",{"id":id})
            updateworking(ll)
            session.pop('id',None)
            if session['info']=='approved':
                return approved()
            elif session['info']=='notapproved':
                return notapproved()
        elif session['activityname']=='seminar':
            db.execute("UPDATE seminar SET status= :status WHERE id=:id",{"status":"yes","id":id})
            print("success")
            db.commit();
            ll=db.execute("SELECT rollno,semester,wdays,lopartic,activityname from seminar WHERE id=:id",{"id":id})
            updateworking(ll)
            session.pop('id',None)
            if session['info']=='approved':
                return approved()
            elif session['info']=='notapproved':
                return notapproved()
        elif session['activityname']=='social':
            db.execute("UPDATE social SET status= :status WHERE id=:id",{"status":"yes","id":id})
            print("success")
            db.commit();
            ll=db.execute("SELECT rollno,semester,wdays,lopartic,activityname from social WHERE id=:id",{"id":id})
            updateworking(ll)
            session.pop('id',None)
            if session['info']=='approved':
                return approved()
            elif session['info']=='notapproved':
                return notapproved()
        elif session['activityname']=='nss':
            db.execute("UPDATE nss SET status= :status WHERE id=:id",{"status":"yes","id":id})
            print("success")
            db.commit();
            ll=db.execute("SELECT rollno,semester,wdays,lopartic,activityname from nss WHERE id=:id",{"id":id})
            updateworking(ll)
            session.pop('id',None)
            if session['info']=='approved':
                return approved()
            elif session['info']=='notapproved':
                return notapproved()

@app.route("/uploads", methods=['GET', 'POST'])
def uploads():
    if not session.get('logged_in'):
        CNFM="please login"
        return render_template('logins.html',CNFM=CNFM)
    else:
        file = request.files['files']
        userss=session['username']
        activityname=session['activityname']
        actreg=session['reg']
        actbranch=session['branch']
        years=int(request.form.get("yearp"))
        sem=int(request.form.get("sem"))
        print(sem)
        activitydes=request.form.get("activityd")
        frdates=request.form.get("frdate")
        todates=request.form.get("todate")
        workings=request.form.get("working")
        levelps=request.form.get("levelp")
        placesps=request.form.get("placep")
        if file and allowed_file(file.filename):
            sen=file.read()
            if(len(sen)<100024):
                if activityname=="cultural":
                    db.execute("INSERT INTO cultural(rollno,reg,branch,year,semester,activityname,activitydesc,fromdate,todate,wdays,lopartic,popartic,img) VALUES (:rollno,:reg,:branch,:year,:semester,:activityname,:activitydesc,:fromdate,:todate,:wdays,:lopartic,:popartic,:img)",{"rollno":userss,"reg":actreg,"branch":actbranch,"year":years,"semester":sem,"activityname":activityname,"activitydesc":activitydes,"fromdate":frdates,"todate":todates,"wdays":workings,"lopartic":levelps,"popartic":placesps,"img":sen})
                    #db.execute("INSERT INTO infors(rollno,activityname,activitydesc,fromdate,todate,lopartic,popartic) VALUES (:rollno,:activityname,:activitydesc,:fromdate,:todate,:lopartic,:popartic)",{"rollno":userss,"activityname":activityname,"activitydesc":activitydes,"fromdate":frdates,"todate":todates,"lopartic":levelps,"popartic":placesps})
                    print("success")
                    db.commit();
                    session.pop('activityname', None)
                    sn="SUCCESSFULLY INSERTED"
                    return render_template('bootlogout.html',sn=sn)
                elif activityname=="literacy":
                    db.execute("INSERT INTO literacy(rollno,reg,branch,year,semester,activityname,activitydesc,fromdate,todate,wdays,lopartic,popartic,img) VALUES (:rollno,:reg,:branch,:year,:semester,:activityname,:activitydesc,:fromdate,:todate,:wdays,:lopartic,:popartic,:img)",{"rollno":userss,"reg":actreg,"branch":actbranch,"year":years,"semester":sem,"activityname":activityname,"activitydesc":activitydes,"fromdate":frdates,"todate":todates,"wdays":workings,"lopartic":levelps,"popartic":placesps,"img":sen})
                    #db.execute("INSERT INTO infors(rollno,activityname,activitydesc,fromdate,todate,lopartic,popartic) VALUES (:rollno,:activityname,:activitydesc,:fromdate,:todate,:lopartic,:popartic)",{"rollno":userss,"activityname":activityname,"activitydesc":activitydes,"fromdate":frdates,"todate":todates,"lopartic":levelps,"popartic":placesps})
                    print("success")
                    db.commit();
                    session.pop('activityname', None)
                    sn="SUCCESSFULLY INSERTED"
                    return render_template('bootlogout.html',sn=sn)
                elif activityname=="sports":
                    db.execute("INSERT INTO sport(rollno,reg,branch,year,semester,activityname,activitydesc,fromdate,todate,wdays,lopartic,popartic,img) VALUES (:rollno,:reg,:branch,:year,:semester,:activityname,:activitydesc,:fromdate,:todate,:wdays,:lopartic,:popartic,:img)",{"rollno":userss,"reg":actreg,"branch":actbranch,"year":years,"semester":sem,"activityname":activityname,"activitydesc":activitydes,"fromdate":frdates,"todate":todates,"wdays":workings,"lopartic":levelps,"popartic":placesps,"img":sen})
                    #db.execute("INSERT INTO infors(rollno,activityname,activitydesc,fromdate,todate,lopartic,popartic) VALUES (:rollno,:activityname,:activitydesc,:fromdate,:todate,:lopartic,:popartic)",{"rollno":userss,"activityname":activityname,"activitydesc":activitydes,"fromdate":frdates,"todate":todates,"lopartic":levelps,"popartic":placesps})
                    print("success")
                    db.commit();
                    session.pop('activityname', None)
                    sn="SUCCESSFULLY INSERTED"
                    return render_template('bootlogout.html',sn=sn)
                elif activityname=="seminar":
                    db.execute("INSERT INTO seminar(rollno,reg,branch,year,semester,activityname,activitydesc,fromdate,todate,wdays,lopartic,popartic,img) VALUES (:rollno,:reg,:branch,:year,:semester,:activityname,:activitydesc,:fromdate,:todate,:wdays,:lopartic,:popartic,:img)",{"rollno":userss,"reg":actreg,"branch":actbranch,"year":years,"semester":sem,"activityname":activityname,"activitydesc":activitydes,"fromdate":frdates,"todate":todates,"wdays":workings,"lopartic":levelps,"popartic":placesps,"img":sen})
                    #db.execute("INSERT INTO infors(rollno,activityname,activitydesc,fromdate,todate,lopartic,popartic) VALUES (:rollno,:activityname,:activitydesc,:fromdate,:todate,:lopartic,:popartic)",{"rollno":userss,"activityname":activityname,"activitydesc":activitydes,"fromdate":frdates,"todate":todates,"lopartic":levelps,"popartic":placesps})
                    print("success")
                    db.commit();
                    session.pop('activityname', None)
                    sn="SUCCESSFULLY INSERTED"
                    return render_template('bootlogout.html',sn=sn)
                elif activityname=="social":
                    db.execute("INSERT INTO social(rollno,reg,branch,year,semester,activityname,activitydesc,fromdate,todate,wdays,lopartic,popartic,img) VALUES (:rollno,:reg,:branch,:year,:semester,:activityname,:activitydesc,:fromdate,:todate,:wdays,:lopartic,:popartic,:img)",{"rollno":userss,"reg":actreg,"branch":actbranch,"year":years,"semester":sem,"activityname":activityname,"activitydesc":activitydes,"fromdate":frdates,"todate":todates,"wdays":workings,"lopartic":levelps,"popartic":placesps,"img":sen})
                    #db.execute("INSERT INTO infors(rollno,activityname,activitydesc,fromdate,todate,lopartic,popartic) VALUES (:rollno,:activityname,:activitydesc,:fromdate,:todate,:lopartic,:popartic)",{"rollno":userss,"activityname":activityname,"activitydesc":activitydes,"fromdate":frdates,"todate":todates,"lopartic":levelps,"popartic":placesps})
                    print("success")
                    db.commit();
                    session.pop('activityname', None)
                    sn="SUCCESSFULLY INSERTED"
                    return render_template('bootlogout.html',sn=sn)
                elif activityname=="nss":
                    db.execute("INSERT INTO nss(rollno,reg,branch,year,semester,activityname,activitydesc,fromdate,todate,wdays,lopartic,popartic,img) VALUES (:rollno,:reg,:branch,:year,:semester,:activityname,:activitydesc,:fromdate,:todate,:wdays,:lopartic,:popartic,:img)",{"rollno":userss,"reg":actreg,"branch":actbranch,"year":years,"semester":sem,"activityname":activityname,"activitydesc":activitydes,"fromdate":frdates,"todate":todates,"wdays":workings,"lopartic":levelps,"popartic":placesps,"img":sen})
                    #db.execute("INSERT INTO infors(rollno,activityname,activitydesc,fromdate,todate,lopartic,popartic) VALUES (:rollno,:activityname,:activitydesc,:fromdate,:todate,:lopartic,:popartic)",{"rollno":userss,"activityname":activityname,"activitydesc":activitydes,"fromdate":frdates,"todate":todates,"lopartic":levelps,"popartic":placesps})
                    print("success")
                    db.commit();
                    session.pop('activityname', None)
                    sn="SUCCESSFULLY INSERTED"
                    return render_template('bootlogout.html',sn=sn)
                sn="its not a valid database"
                return render_template("bootlogout.html",sn=sn)
            else:
                sn="oops! photosize must less than 100kb"
                return render_template("bootlogout.html",sn=sn)
        else:
            sn="oops! Insert photo only"
            return render_template("bootlogout.html",sn=sn)


@app.route("/download", methods=['GET', 'POST'])
def download():
    images=db.execute("SELECT encode(img::bytea, 'base64') from images where imgid = 1").fetchall()
    for i in images:
        print(i)
        for k in i:
            print(k)
            return render_template("fail.html",k=k)
if __name__=='__main__':
    from werkzeug.serving import run_simple
    app.secret_key = os.urandom(12)
    run_simple('localhost',9000,app)