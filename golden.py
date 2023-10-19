import pymysql

conn = None
cur = None

data1=""
data2=""
data3=""
data4=""

sql = ""

conn = pymysql.connect(host='127.0.0.1', user='root', password='2021011545', db='news', charset='utf8')
cur = conn.cursor()

while(True):
    data1 = input("채널 ID: ")
    if data1 == "":
        break;
    data2 = input("비디오 ID: ")
    data3 = input("제목: ")
    data4 = input("내용: ")
    sql = "INSERT INTO news (channel_id, video_id, title, summary) VALUES(%s, %s, %s, %s)"
    values = (data1, data2, data3, data4)
    cur.execute(sql, values)

conn.commit()
conn.close()
