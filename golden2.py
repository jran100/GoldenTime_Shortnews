import pymysql

conn = None
cur = None

data1=""
data2=""
data3=""
data4=""

row = None

conn = pymysql.connect(host='127.0.0.1', user='root', password='2021011545', db='news', charset='utf8')
cur = conn.cursor()

cur.execute("SELECT * FROM news")

print("    방송사    |    비디오번호    |      제목      |      요약      ")
print("===============================================================")

while(True):
    row = cur.fetchone()
    if row == None:
        break
    data1 = row[1]
    data2 = row[2]
    data3 = row[3]
    data4 = row[4]
    print("%5s  %15s  %15s  %15s" % (data1, data2, data3, data4))

conn.close()