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
                file.write(self.today)
            return True

        else:
            return False

    def update_news(self, broadcastName, broadcastID, maxResults):
        if True:  # self.isTime():
            gpt_client = ChatGPTClient()
            youtube_client = YoutubeClient()
            db_manager = DBManager()

            videos = youtube_client.request_video_info(broadcastID, maxResults)
            
            for video in videos:
                video_id = video["id"]
                title = video["title"]
                thumbnail = video['thumbnail']
                url = video['url']
                transcript = youtube_client.request_transcript(video_id)
                summary = gpt_client.request_summary(transcript)

                #video_info.append({"id": video_id, "title": title, "thumbnail": thumbnail, "url": f"/play_video/{video_id}"})

                #DB에 뉴스 정보 업데이트, url 빼기
                db_manager.insert_data(broadcastName, video_id, title, thumbnail, summary)

            return

        else:
            return



#broad cast ID로 사용
mbc_id = "UCF4Wxdo3inmxP-Y59wXDsFw" #MBC
ytn_id = "UChlgI3UHCOnwUGzWzbJ3H5w" #YTN
kbs_id = "UCcQTRi69dsVYHN3exePtZ1A" #KBS
sbs_id = "UCkinYTS9IHqOEwR1Sze2JTw" #SBS


if __name__ == '__main__':
    update = Updater()
    update.update_news('MBC', mbc_id, 10)
    #update.update_news('YTN', mbc_id, 10)
    #update.update_news('KBS', mbc_id, 10)
    #update.update_news('SBS', mbc_id, 10)
    


"""

db_manager.select_all()
print("Select All executed")
db_manager.select_broadcast(broadcastName)
print(f"Select Broad executed for {broadcastName}")

"""


