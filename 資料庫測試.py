import pymysql
import csv


db = pymysql.connect(host="localhost",port=3306,user="root",password="kimmki",db="covid-19",charset="utf8")
cursor = db.cursor() 

sql = """INSERT INTO num 
         (date,南投縣,台中市,台北市,台南市,台東縣,嘉義市,嘉義縣,基隆市,境外移入,宜蘭縣,屏東縣,彰化縣,新北市,新竹市,新竹縣,桃園市,澎湖縣,花蓮縣,苗栗縣,連江縣,金門縣,雲林縣,高雄市)
         VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

start = 0         
csvfile = "covid_19 data.csv"
with open(csvfile, 'r') as fp:
    reader = csv.reader(fp)
    insert_data=list()
    for row in reader:
        if(start==0):
            start = 1
            continue
        a_record = tuple(row)
        insert_data.append(a_record)
        print(row)
        
cursor.executemany(sql,insert_data)
db.commit()
    
    
db.close()