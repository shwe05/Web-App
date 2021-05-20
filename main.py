from flask import Flask, render_template,request
app = Flask(__name__)
import datetime
import sqlite3 

'------------------------------------------------------------------------------'
@app.route('/')
def hello(): 
    return render_template('hello.html')


'------------------------------------------------------------------------------'

@app.route('/register')
def register():
    return render_template('register.html') 

'------------------------------------------------------------------------------'

@app.route('/login',methods=['GET','POST'])
def login():
    return render_template('existing.html')

'------------------------------------------------------------------------------'
@app.route('/homepage')
def home():
    return render_template('homepage.html') 


'------------------------------------------------------------------------------'
@app.route('/homepage',methods=['GET','POST'])
def register_page():
    username = request.form.get('UserName')
    userid = request.form.get('UserID')
    number = request.form.get('PhoneNumber')
    password = request.form.get('Pass')
    useremail = request.form.get('Email')

    db = sqlite3.connect('stickers.db')

    c = db.cursor()

    c.execute('''INSERT INTO user(UserID,UserName,UserEmail,UserNumber,UserPassword)
       VALUES (:UserID,:UserName,:UserEmail,:UserNumber,:UserPassword)''',
    {"UserID":userid,"UserName":username,"UserEmail":useremail,"UserNumber":number,
     "UserPassword":password})
    db.commit()
    return render_template('homepage.html',username=username,userid=userid)

'------------------------------------------------------------------------------'

userid = '' #So that other functions can use it! 

@app.route('/loginpage',methods=['GET','POST'])
def login_page():

    
    global userid #Takes from this function 

    
    userid = request.form.get('UserID')
    password = request.form.get('Pass')
    db = sqlite3.connect('stickers.db')
    c = db.cursor()
    c.execute('''SELECT UserID,UserPassword,UserName FROM user WHERE UserID=?''',(userid,))
    data = list(c.fetchone())
    if userid == data[0] and password == data[1]:
        
        return render_template('homepage.html',username=data[2])
    elif userid == data[0] and password != data[1]:
        return render_template('existing.html')
    else:
        return render_template('register.html')

'------------------------------------------------------------------------------'  
@app.route('/shopping') 
def shop():
    db = sqlite3.connect('stickers.db')
    c = db.cursor()
    c.execute('''SELECT StickerName , StickerID FROM stickers''')
    sticker = c.fetchall()

    d = db.cursor()
    d.execute('''SELECT UserName FROM user WHERE UserID=?''',(userid,))
    name = list(d.fetchone())
    
    return render_template('shop.html',sticker=sticker,name=name[0])

'------------------------------------------------------------------------------'

stickers_selected = ''
total = 0 
@app.route('/cart',methods=['GET','POST'])
def cart():
    global stickers_selected
    global total
    db = sqlite3.connect('stickers.db')
    c = db.cursor()
    c.execute('''SELECT UserName FROM user WHERE UserID=?''',(userid,))
    name = list(c.fetchone())
    stickers_selected = request.form.getlist('select_sticker')
    s = []
    ids = []
    for i in stickers_selected:
        s.append(i.split('-'))
    for i in s:
        ids.append(i[1])

    total = 0
    d = db.cursor()
    while len(ids) != 0:
        d.execute('''SELECT StickerPrice FROM stickers WHERE StickerID=?''',(ids[0],))
        price = list(d.fetchone())
        total += price[0]
        ids = ids[1:]
    

    return render_template('cart.html',stickers_selected = stickers_selected,total=total,name=name[0]) 

'------------------------------------------------------------------------------'
@app.route('/confirmedcart',methods=['GET','POST'])
def confirmed():
    db = sqlite3.connect('stickers.db')
    c = db.cursor()
    c.execute('''SELECT UserName,UserID,UserEmail,UserNumber FROM user WHERE UserID=?''',(userid,))
    user_data = list(c.fetchone())
    date = datetime.datetime.now()

    d = db.cursor()
    d.execute('''INSERT INTO purchase(UserID,TotalPrice)
                VALUES(:UserID,:TotalPrice)''',{"UserID":user_data[1],
                                                    "TotalPrice":total})
    db.commit()
    
        
    
    db.close() 
    
    return render_template('confirmed.html',name=user_data[0],userid=user_data[1],
                           email=user_data[2],number=user_data[3],date=date,total=total,
                           stickers_selected=stickers_selected) 
    

'------------------------------------------------------------------------------'

 
app.run(debug=True,port=5011)

