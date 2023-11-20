from datetime import datetime
from ChatGPTClient import ChatGPTClient
from YoutubeClient import YoutubeClient
from DBManager import DBManager

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
        if True: #self.isTime():
            gpt_client = ChatGPTClient()
            youtube_client = YoutubeClient()
            #DBManager 객체 생성
            video_info = youtube_client.request_video_info(broadcastID, maxResults)
            for video in video_info:
                video_id = video["id"]
                transcript = youtube_client.request_transcript(video_id)
                summary = gpt_client.request_summary(transcript)

                #데이터 매니저 호출하여 데이터 저장할 것.
                
                #dbmanager.save_data(broadcastName, video['id'], video['title'], video['thumbnail'], video['url'], summary)

                print(broadcastName)
                print(video['id'])
                print(video['title'])
                print(video['thumbnail'])
                print(video['url'])
                print(summary)

            return

        else:
            return
        


#broad cast ID로 사용
mbc_id = "UCF4Wxdo3inmxP-Y59wXDsFw" #MBC
ytn_id = "UChlgI3UHCOnwUGzWzbJ3H5w" #YTN
kbs_id = "UCcQTRi69dsVYHN3exePtZ1A" #KBS
sbs_id = "UCkinYTS9IHqOEwR1Sze2JTw" #SBS

update = Updater()
update.update_news('MBC', mbc_id, 8)



            

            

