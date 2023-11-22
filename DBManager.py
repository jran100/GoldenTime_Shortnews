import pymysql

class DBManager:
    def __init__(self):
        self.db = pymysql.connect(host='127.0.0.1', user='Golden1', password='Q1886e', db='news', charset='utf8')

    def insert_data(self, broadcastName, video_id, title, thumbnail, url, summary):
        try:
            cur = self.db.cursor()
            setdata = (broadcastName, video_id, title, thumbnail, url, summary)
            query = "INSERT INTO news(broadcastName, video_id, title, thumbnail, url, summary) VALUES(%s, %s, %s, %s, %s, %s)"
            cur.execute(query, setdata)
            self.db.commit()
        except Exception as e:
            print("db error", e)
        finally:
            if cur:
                cur.close()
            """if self.db:
                self.db.close()"""

    def select_all(self):
        ret = []
        try:
            with self.db.cursor() as cur:
                query = "SELECT * FROM news"
                cur.execute(query)
                rows = cur.fetchall()
                """for e in rows:
                    news = {'broadcastName': e[0], 'video_id': e[1], 'title': e[2], 'thumbnail': e[3], 'url': e[4], 'summary': e[5]}
                    ret.append(news)"""
                for row in rows:
                    print(row)
        except pymysql.Error as e:
            print('db error', e)
        finally:
            return ret

    def select_broad(self, broadcastName):
        #ret = ()
        try:
            with self.db.cursor() as cur:
                query = "SELECT * FROM news WHERE broadcastName = %s"
                cur.execute(query, (broadcastName, ))
                rows = cur.fetchall()
                for row in rows:
                    print(row)
        except pymysql.Error as e:
            print('db error', e)
        finally:
            return