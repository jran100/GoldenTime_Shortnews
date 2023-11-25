from datetime import datetime
from summary import ChatGPTClient
from summary import YoutubeClient
from manager import DBManager

class Updater():
    def __init__(self):
        self.log_path = "log.txt"

    def isTime(self):
        today = datetime.now().strftime("%Y-%m-%d")
        with open(self.log_path, "r") as file:
            lines = file.readlines()
            last_date = lines[-1].strip()
        if today != last_date:
            with open(self.log_path, "w") as file:
                file.write(today)
            return True

        else:
            return False

    def update_news(self, broadcastName, broadcastID, maxResults):
        #하루에 한번 업데이트
        gpt_client = ChatGPTClient()
        youtube_client = YoutubeClient()
        db_manager = DBManager()

        videos = youtube_client.request_video_info(broadcastID, maxResults)
            
        for video in videos:
            video_id = video["id"]
            title = video["title"]
            thumbnail = video['thumbnail']
            transcript = youtube_client.request_transcript(video_id)
            summary = gpt_client.request_summary(transcript)
            #DB에 뉴스 업데이트
            db_manager.insert_data(broadcastName, video_id, title, thumbnail, summary)

        return





#broad cast ID로 사용
mbc_id = "UCF4Wxdo3inmxP-Y59wXDsFw" #MBC
ytn_id = "UChlgI3UHCOnwUGzWzbJ3H5w" #YTN
kbs_id = "UCcQTRi69dsVYHN3exePtZ1A" #KBS
sbs_id = "UCkinYTS9IHqOEwR1Sze2JTw" #SBS


if __name__ == '__main__':
    update = Updater()
    if update.isTime():
        update.update_news('MBC', mbc_id, 30)
        #update.update_news('SBS', sbs_id, 30)
    

