from flask import Flask,render_template,request,redirect,url_for,flash#,jsonify,session
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,DateTimeField,SubmitField
from wtforms.validators import InputRequired,Length
import matplotlib.pyplot as plt

import pymysql
import io
import base64
import time
import os

db = pymysql.connect("127.0.0.1","root","1qaz1qaz","PTQS1005" )
cursor = db.cursor()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24) 

class dateform(FlaskForm):                   #抓到時
    entrydate1 = DateTimeField('查詢的初始時間',format='%Y-%m-%d %H',validators=[InputRequired(message=u'查詢的初始時間未填')])#format='%Y-%m-%d %H:%M:%S'
    entrydate2 = DateTimeField('查詢的結束時間',format='%Y-%m-%d %H',validators=[InputRequired(message=u'查詢的結束時間未填')])#format='%Y-%m-%d %H:%M:%S'
    #name = StringField('name')   #從這裡取表單的東西,StringField取字串
    #password = PasswordField('password')#PasswordField取密碼
    submit = SubmitField(u'確認')


@app.route('/',methods=['GET','POST'])
def times():
    form = dateform()
    
    if form.validate_on_submit():  #點擊按鈕
        
        print(form.entrydate1.data)
        print(form.entrydate2.data)
        cursor.execute("SELECT * FROM ptqs WHERE create_time BETWEEN '" + str(form.entrydate1.data) + "' AND '" + str(form.entrydate2.data) + "'")
        A=cursor.fetchall()
        print(A)

        if not A:
            flash(u'資料庫沒有此時間')
            print('資料庫沒有此時間')
            return redirect(url_for('time'))
        else :
            
            #return redirect(url_for("data", entrydate1= str(form.entrydate1.data) , entrydate2= str(form.entrydate2.data)))
            return redirect(url_for("plot", entrydate1= str(form.entrydate1.data) , entrydate2= str(form.entrydate2.data)))
            #下面是錯的
    
    
    return render_template('time.html',form=form)


@app.route('/plot')
def plot():    
    
    img = io.BytesIO()
    #cursor.execute("SELECT * FROM pms WHERE create_time BETWEEN '2018-07-09 22:54:21' AND '2018-07-09 22:55:11'")
    print("SELECT * FROM ptqs WHERE create_time BETWEEN '" + str(request.args.get('entrydate1')) + "' AND '" + str(request.args.get('entrydate2')) + "'")
    a = "SELECT * FROM ptqs WHERE create_time BETWEEN '" + str(request.args.get('entrydate1')) + "' AND '" + str(request.args.get('entrydate2')) + "'"
    cursor.execute(a)    
    listpm25=[]
    listTVOC=[]
    listHCHO=[]
    listCO2=[]
    listtem=[]
    listhum=[]
    create_time=[]
    i=0
    for row in cursor.fetchall():
        #print(row[7].strftime('%Y-%m-%d %H:%M:%S'))
        listpm25.append(int(row[1]))
        listTVOC.append(int(row[2]))
        listHCHO.append(int(row[3]))
        listCO2.append(int(row[4]))
        listtem.append(int(row[5]))
        listhum.append(int(row[6]))
        create_time.append(row[7].strftime('%Y-%m-%d %H:%M:%S'))
        #create_time.append(row[7].strftime('%H:%M:%S'))
        i=i+1
    db.commit()
    db.rollback()
    #db.close

    print('listpm25',listpm25)
    print('listTVOC',listTVOC)
    print('listHCHO',listHCHO)
    print('listCO2',listCO2)
    print('listtem',listtem)
    print('listhum',listhum)
    print('create_time',create_time)
    print('i',i)
    #return u'測試'

    #x = [1,2,3,4,5]
    #y = [1,2,3,4,5]
    plt.cla()#加這個 圖片就不會一直疊
    plt.plot(create_time,listpm25, 'o-', label=u'pm25')
    plt.plot(create_time,listTVOC, 'o-', label=u'揮發性有機物')
    plt.plot(create_time,listHCHO, 'o-', label=u'甲醛')

    plt.plot(create_time,listCO2, 'o-', label=u'二氧化碳:')
    plt.plot(create_time,listtem, 'o-', label=u'溫度')
    plt.plot(create_time,listhum, 'o-', label=u'濕度')

    
    plt.gcf().set_size_inches(i+5,6)  #調整大小 先常在高 先Y軸在X軸 有點怪 把長度改成回全浮動 設未知數在上面 a=a++
    plt.xticks(create_time,rotation=15) #=90是直的 但是底下會被切掉 原因不明
    plt.xlabel('date-time')
    plt.ylabel(u'微克/立方公尺')
    plt.legend(loc='upper right')
    plt.savefig(img, format='png')
    img.seek(0)
                                                                #getvalue()
    plot_url = base64.b64encode(img.getvalue()).decode()        #使用Base64格式解碼或編碼二進制數據
                                                                #encode:編碼 decode:解碼
    return render_template('plot.html', plot_url=plot_url)
    

if __name__ == '__main__':
    app.run(port=9000,debug =True)
