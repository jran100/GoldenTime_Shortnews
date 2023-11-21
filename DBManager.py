import pymysql

class DBManager:
    def __init__(self, number):
        self.num = number
db= None
cur = None

def insert_data(broadcastName, video_id, title, url, summary):
    try:
        db = pymysql.connect(host='127.0.0.1', user='root', password='2021011545', db='news', charset='utf8')
        cur = db.cursor()
        setdata = (broadcastName, video_id, title, url, summary)
        cur.execute("INSERT INTO news (broadcastName, video_id, title, url, summary) VALUES(%s, %s, %s, %s, %s", setdata)
        db.commit()
    except Exception as e:
        print("db error", e)
    finally:
        db.close()
def select_all():
    ret = []
    try:
        db = pymysql.connect(host='127.0.0.1', user='root', password='2021011545', db='news', charset='utf8')
        cur = db.cursor()
        cur.execute("SELECT * FROM news")
        rows = cur.fetchall()
        for e in rows:
            news = {'broadcastName': e[0], 'video_id': e[1], 'title' : e[2], 'url': e[3], 'summary': e[4]}
            ret.append(news)
    except Exception as e:
        print('db error', e)
    finally:
        db.commit()
        db.close()
        return ret
def select_broad(self, broadcastName):
    ret = ()
    try:
        db = pymysql.connect(host='127.0.0.1', user='root', password='2021011545', db='news', charset='utf8')
        cur = db.cursor()
        setdata = (broadcastName, )
        cur.execute('SELECT * FROM news WHERE broadcastName = %s', setdata)
        ret = cur.fetchone()
    except Exception as e:
        print('db error', e)
    finally:
        db.close()
        return ret