import serial
import time
from datetime import datetime
ser = serial.Serial('COM7', 9600, timeout=0.5)
import pymysql

db = pymysql.connect("127.0.0.1","root","1qaz1qaz","PTQS1005" )

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用 execute() 方法执行 SQL，如果表存在则删除
cursor.execute("DROP TABLE IF EXISTS ptqs")

# 使用预处理语句创建表
ptqs="""CREATE TABLE ptqs ( 
         number Integer NOT NULL AUTO_INCREMENT,
         pm25 INT,
         TVOC INT,  
         HCHO INT,
         CO2 INT,
         tem INT,
         hum INT,
         create_time DATETIME, 
         PRIMARY KEY (number))"""
cursor.execute(ptqs)

def ptq():    
    ser.write(b'\x42\x4D\xAB\x00\x00\x01\x3A')
    
    time.sleep(0.1)    
    pm25L=0
    TVOCL=0
    HCHOL=0
    CO2L=0
    temL=0
    humL=0
    h=0
    pm25=0
    TVOC=0
    HCHO=0
    CO2=0
    tem=0
    hum=0
    i = 0
    while True:
        h=ser.read()#
        time.sleep(0.1)
        print('count',i)
        print('ser.read()',h)
        h=int.from_bytes(h, byteorder='little')
        
        if i== 4:            
            pm25L=ser.read()
            #time.sleep(0.5)
            print('pm25L',pm25L)            
            print("\n")
            pm25L=int.from_bytes(pm25L, byteorder='little')
            print('pm25L',pm25L)
            pm25=h*256+pm25L
            print('PM2.5:' ,pm25,'ug/m3')
            print("\n")
            i=i+1
        if i==6:          
            TVOCL=ser.read()
            #time.sleep(0.5)            
            print('TVOCL',TVOCL)
            print("\n")
            TVOCL=int.from_bytes(TVOCL, byteorder='little')
            print('TVOCL',TVOCL)
            TVOC=h*256+TVOCL
            print('揮發性有機物TVOC:' ,TVOC , 'ppb')
            print("\n")
            i=i+1

        if i==9:
            HCHOL=ser.read()
            #time.sleep(0.5)
            print('HCHOL',HCHOL)
            print("\n")
            HCHOL=int.from_bytes(HCHOL, byteorder='little')
            print('HCHOL',HCHOL)
            HCHO=h*256+HCHOL
            print('甲醛:' , HCHO,'ug/m3')
            print("\n")
            i=i+1
         
        if i==12:
            CO2L=ser.read()
            #time.sleep(0.5)
            print('CO2L',CO2L)
            print("\n")
            CO2L=int.from_bytes(CO2L, byteorder='little')
            print('CO2L',CO2L)
            CO2=h*256+CO2L
            print('二氧化碳:' ,CO2,'ppm')
            print("\n")
            i=i+1
        if i==14:
            temL = ser.read()
            #time.sleep(0.5)
            print('temL',temL)
            print("\n")
            temL=int.from_bytes(temL, byteorder='little')
            print('temL',temL)
            tem=(h*256+temL)/10.0
            print('溫度:',tem)
            print("\n")
            i=i+1 
            
        if i==16:
            humL = ser.read()
            #time.sleep(0.5)
            print('humL',humL)
            print("\n")
            humL=int.from_bytes(humL, byteorder='little')
            print('humL',humL)
            hum=(h*256+humL)/10.0
            print('濕度:',hum)
            print("\n")
            i=i+1

        i = i + 1        
        if i==24:
            create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(str(create_time)) 
            cursor.execute("INSERT INTO ptqs (pm25, TVOC, HCHO, CO2, tem, hum, create_time) VALUES (" + str(pm25) + ", " + str(TVOC) + ", " + str(HCHO) + ", " + str(CO2) + ", " + str(tem) + ", " + str(hum) + ", '" + str(create_time) + "')")
            db.commit()
            db.rollback()  
            break




#ptq()
count = 1
while True:
    ptq()

    if(count==5):
        print("取出5次")
        break
    count=count+1