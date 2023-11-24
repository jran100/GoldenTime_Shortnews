
import pymysql

class DBManager():
    def __init__(self):
        self.db = pymysql.connect(host='127.0.0.1', port=3307, user='shortnews', password='goldentime1234', db='news', charset='utf8')

    def insert_data(self, broadcastName, video_id, title, thumbnail, summary):
        video_id_list = self.select_all_video_id()
        if video_id not in video_id_list:
            try:
                cur = self.db.cursor()
                setdata = (broadcastName, video_id, title, thumbnail, summary)
                query = "INSERT INTO news(broadcastName, video_id, title, thumbnail, summary) VALUES(%s, %s, %s, %s, %s)"
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

    def select_all(self):
        '''
        방송사 상관없이 모든 뉴스 영상 가져오기
        '''
        ret = []
        try:
            with self.db.cursor() as cur:
                query = "SELECT video_id, title, thumbnail FROM news" #추가수정
                cur.execute(query)
                rows = cur.fetchall()
                for e in rows:
                    news = {'video_id': e[0], 'title': e[1], 'thumbnail': e[2]}
                    ret.append(news)
                
                #for row in rows:
                    #print(row)
        except pymysql.Error as e:
            print('db error', e)
        finally:
            return ret

    def select_broadcast(self, broadcastName):
        '''
        특정 방송사에 대한 뉴스 영상만 가져오기
        '''
        ret = []
        try:
            with self.db.cursor() as cur:
                query = "SELECT video_id, title, thumbnail FROM news WHERE broadcastName = %s" #추가수정
                cur.execute(query, (broadcastName, ))
                rows = cur.fetchall()
                for e in rows:
                    news = {'video_id': e[0], 'title': e[1], 'thumbnail': e[2]}
                    ret.append(news)
                #for row in rows:
                    #print(row)

        except pymysql.Error as e:
            print('db error', e)
        finally:
            return ret
        
    def select_summary(self, video_id):
        try:
            with self.db.cursor() as cur:
                query = "SELECT video_id, title, summary FROM news WHERE video_id = %s"
                cur.execute(query, (video_id, ))
                rows = cur.fetchall()
                e = rows[0]
                summarized_news = {'video_id': e[0], 'title': e[1], 'summary': e[2]}

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

        for attr in video_id_tuple:
            video_id_list.append(attr[0])


        return video_id_list


    

class NewsManager():
    def __init__(self):
        self.db_manager = DBManager()

    def request_news(self, broadcastName):
        videos = self.db_manager.select_broadcast(broadcastName)
        return videos

    def request_all_news(self):
        videos = self.db_manager.select_all()
        return videos
    
    def request_summary(self, video_id):
        summarized_news = self.db_manager.select_summary(video_id)
        return summarized_news

        

