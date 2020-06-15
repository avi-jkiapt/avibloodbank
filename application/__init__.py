from flask import Flask,render_template,request,redirect,url_for,session,flash
import json
import os

app = Flask(__name__)
app.debug =True
app.secret_key ='sjidakqntasnditoaqwertyuioplkhgsgdaszxcvbnmkloiywyy273gdtmdk'

@app.route('/')
def home():
    if 'username' in session:
        #if session['username']:
        print(session['username'])
        return render_template('home.html',username=session['username'])
    return render_template('home.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method =='POST':
        allUsers ={}
        error=None
        with open('users.json') as readfile:
            allUsers = json.load(readfile)

        password =request.form['pwd']
        #print(request.form['email'])
        bbdid =request.form['email']
        utype =request.form.get('typeU')
        
        print(allUsers.keys())
        if bbdid not in allUsers.keys():
            print('Users does not exist')
            error ='Users does not exist'
            return render_template('login.html',error=error)
            
        else:
            user =allUsers[bbdid]
            
            pwd =user['pwd']
            userId =user['bbdid']
            userType =user['usertype']
            if (pwd ==password and userId == bbdid) and userType ==utype :
                print("You loggedd in successfully")
                session['username']=bbdid
                #session['password']=password
                session['usertype'] =userType
                flash('You Successfully logged in')
                return redirect(url_for('home'))
            else:
                print('Either bbdid or pwd is wrong')
                error ='Either bbdid or pwd is wrong'
                return render_template('login.html',error=error)
    return render_template('login.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method =='POST':
        error=None
        allUser ={}
        #print("hello golu" + str(os.path.exists('users.json')))
        if os.path.exists('users.json'):
            with open('users.json') as urls_file:
                allUser = json.load(urls_file)
        
        bbdid =request.form.get('username')
        pwd=request.form['pwd']
        usertype=request.form.get('usertype')
        firstname =request.form['firstname']
        contact =request.form['number']
        address=request.form.get('address')
        bgroup =request.form['bgroup']
        dob =request.form['dob']
        age=request.form['age']
        ioeName =request.form['ioeName']
        ioeNumber =request.form['ioeNumber']
        ioeRelation =request.form['ioeRelation']
        users ={}
        
        
        #avi=[]
        #print(bbdid)
        users['bbdid'] =bbdid
        users['pwd'] =pwd
        users['usertype']=usertype
        users['firstname'] =firstname
        users['contact'] =contact
        users['address']=address
        users['bgroup'] =bgroup
        users['dob'] =dob
        #allUser ={}
        if bbdid in allUser.keys():
            #print('ALready userid taken plz use other')
            error ='ALready userid taken plz use other'
            #flash('ALready userid taken plz use other')
            return render_template('register.html',error=error)
        allUser[bbdid] =users
        with open('users.json','w') as userfile:
            json.dump(allUser,userfile)
            #userfile.write(avi)
        session['username']=bbdid
        #session['password']=pwd
        session['usertype'] =usertype
        flash('You logged innn')
        return redirect(url_for('home',username=bbdid))
    return render_template('register.html')

@app.route('/search')
def search():
    if 'username' in session:
        #print(session['username'])
        return render_template('search.html',allValue =session)
    
    return render_template('search.html',allValue=None)


@app.route('/searchParameter')
def searchwithparameter():
    bbdid =request.args.get('bbdid')
    users ={}
    user ={}
    with open('users.json') as readfile:
        users =json.load(readfile)
    if bbdid in users.keys():
        user =users[bbdid]
    else:
        user =None
    print(user)
    if 'username' in session:
        return render_template('result.html',user =user,username=session['username'])
    else:
        return render_template('result.html',user=user,username =None)

@app.route('/searchBloodGroup')
def searchBG():
    blood =request.args.get('bgroup')
    users ={}
    with open('users.json') as readfile:
        users =json.load(readfile)
    userMatch =[]
    allPerson =[]
    for bbdid,user in users.items():
        allPerson.append(user)
    for user in allPerson:
        if user['bgroup'] == blood:
            userMatch.append(user)
    #print(userMatch)
    return render_template('resulttwo.html',username =session['username'],userMatch=userMatch)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))
