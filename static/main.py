from flask import Flask, render_template,request
app = Flask(__name__)
import datetime
import sqlite3 




@app.route('/')
def login():
    return render_template('register.html')

@app.route('/shopping') 
def shop():
    return render_template('shop.html')


@app.route('/homepage',methods=['GET','POST'])
def register_page():
    username = request.form.get('UserName')
    userid = request.form.get('UserID')
    number = request.form.get('PhoneNumber')
    password = request.form.get('Pass')
    useremail = request.form.get('Email')

    db = sqlite3.connect('stickers.db')

    c = db.cursor()


    c.execute('''SELECT UserID from user where UserID=?''',(userid,))
    data =c.fetchall()
    if not data:
        c.execute('''INSERT INTO user(UserID,UserName,UserEmail,UserNumber,UserPassword)
           VALUES (:UserID,:UserName,:UserEmail,:UserNumber,:UserPassword)''',
        {"UserID":userid,"UserName":username,"UserEmail":useremail,"UserNumber":number,
         "UserPassword":password})
        db.commit()
        return render_template('homepage.html',username=username,userid=userid)
    if data:
        return render_template('existing.html')

@app.route('/homepage')


@app.route('/login',methods=['GET','POST'])
def login():
    return render_template('existing.html')




def login_page():
    
##
##    userid = request.form.get('UserID')
##    password = request.form.get('Pass')
##    db = sqlite3.connect('stickers.db')
##    c = db.cursor()
##    c.execute('''SELECT UserPassword FROM user WHERE UserID=?''',(userid,))
##    data = c.fetchall()
##    if data != password:
##        return render_template('incorrect.html')
##    if data == password: 
##        c.execute('''SELECT UserName FROM user WHERE UserID=?''',(userid,))
##        username = c.fetchall()
##        return render_template('homepage.html',username=username,userid=userid) 
    
    userid = request.form.get('UserID')
    password = request.form.get('Pass')
    db = sqlite3.connect('sticker.db')
    c = db.cursor()
    
app.run(debug=True,port=5001)

