import mysql.connector
import random
import time
import csv
from datetime import datetime
import os

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "1234",
    database = "temp"
)

cursor = db.cursor()

def rand():
    return round(random.uniform(50,90),2)

def save(temp,status):
    sql = """
    INSERT INTO temp(temp,status)
    VALUES(%s,%s)
    """
    val = (temp,status)
    cursor.execute(sql,val)
    db.commit()



def avg():
    cursor.execute("SELECT AVG(temp) FROM temp")
    result_avg = cursor.fetchone()[0]
    return round(result_avg,2)

def max_temp():
    cursor.execute("SELECT MAX(temp) FROM temp")
    result_max = cursor.fetchone()[0]
    return round(result_max,2)

def danger_count():
    cursor.execute("SELECT COUNT(*) FROM temp WHERE temp >= 80")
    result_count = cursor.fetchone()[0]
    return round(result_count,2)

def danger_rate():
    cursor.execute("SELECT COUNT(*) FROM temp")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM temp WHERE temp >= 80")
    danger = cursor.fetchone()[0]

    return round((danger/total)*100,2)


# csv 저장 함수
def save_csv(temp,status):
    with open("sensor_log.csv","a",newline="")as file:
        writer = csv.writer(file)
        writer.writerow([
            temp,
            status,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ])

if not os.path.exists("sensor_log.csv"):
    with open("sensor_log.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "temp",
            "status",
            "time"
        ])


while True:
    temp = rand()
    print(f"현재 온도 : {temp}")
    
    status = "DANGER" if temp >=80 else "NORMAL"
    save(temp,status)
    save_csv(temp,status)

    if temp >= 80:
        print("**위험 온도 감지!**\n")
    else:
        print("정상 상태\n")

    print(f"평균 온도 : {avg()}")
    print(f"최고 온도 : {max_temp()}")
    print(f"위험 온도 개수: {danger_count()}")
    print(f"-> 위험률 {danger_rate()}%")
    print("----------------")

    time.sleep(3)    


