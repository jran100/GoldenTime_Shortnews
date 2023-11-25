
import pymysql

class DBManager():
    """
    데이터 베이스에 데이터를 저장, 검색하는 메소드를 가지고 있다

    Attributes:
        db: pymysql.connections.Connection가 반환한 객체
    """
    def __init__(self):
        self.db = pymysql.connect(host='127.0.0.1',
                                  port=3307,
                                  user='shortnews',
                                  password='goldentime1234',
                                  db='news',
                                  charset='utf8')

    def insert_data(self, broadcastName, video_id, title, thumbnail, summary):
        video_id_list = self.select_all_video_id()
        if video_id not in video_id_list:
            try:
                cur = self.db.cursor()
                setdata = (broadcastName, video_id, title, thumbnail, summary)
                query = "INSERT INTO news(broadcastName, video_id, title, thumbnail, summary)\
                    VALUES(%s, %s, %s, %s, %s)"
                
                cur.execute(query, setdata)
                self.db.commit()

            except Exception as e:
                print("db error", e)

            finally:
                if cur:
                    cur.close()
        else:
            pass

        return


    def select_broadcast(self, broadcastName) -> list:
        ret = []
        try:
            with self.db.cursor() as cur:
                query = "SELECT video_id, title, thumbnail FROM news WHERE broadcastName = %s"
                cur.execute(query, (broadcastName, ))
                rows = cur.fetchall()
                for row in rows:
                    news = {'video_id': row[0],
                            'title': row[1],
                            'thumbnail': row[2],
                            'url': f"/play_video/{row[0]}"}
                    
                    ret.append(news)

        except pymysql.Error as e:
            print('db error', e)
        finally:
            return ret
        
    def select_summary(self, video_id) -> dict:
        try:
            with self.db.cursor() as cur:
                query = "SELECT video_id, summary FROM news WHERE video_id = %s"
                cur.execute(query, (video_id, ))
                rows = cur.fetchall()
                row = rows[0]
                summarized_news = {'video_id': row[0], 'summary': row[1]}

        except pymysql.Error as e:
            print('db error', e)
        finally:
            return summarized_news
        
    def select_all_video_id(self):
        video_id_list = []
        try:
            with self.db.cursor() as cur:
                query = "SELECT video_id FROM news"
                cur.execute(query)
                video_id_tuple = cur.fetchall()

        except pymysql.Error as e:
            print('db error', e)

        for id_attribute in video_id_tuple:
            video_id_list.append(id_attribute[0])

        return video_id_list


    

class NewsManager():
    """
    DBMananger에게 뉴스 데이터 저장, 검색을 요청하는 메소드가 구현되어 있다.

    Attributes:
        db_manager: DBManager 객체
    """
    def __init__(self):
        self.db_manager = DBManager()

    def request_news(self, broadcastName):
        videos = self.db_manager.select_broadcast(broadcastName)
        return videos

    def request_all_news(self):
        videos = self.db_manager.select_all_video_id()
        return videos
    
    def request_summary(self, video_id):
        summarized_news = self.db_manager.select_summary(video_id)
        return summarized_news

        

