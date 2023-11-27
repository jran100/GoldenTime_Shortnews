from datetime import datetime

from summary import ChatGPTClient
from summary import YoutubeClient

from manager import DBManager

class Updater():
    """
    Youtube Client, Chat GPT Client 클래스에게 영상정보를 요청하고,
    받은 데이터를 데이터 베이스에 업데이트하는 클래스
    *로그 파일에 저장된 이전 업데이트 날짜를 바탕으로 현재 날짜와 비교하여
    값이 다른 경우에만 업데이트 함*

    Attributes:
        log_path: 로그파일의 경로를 저장하는 멤버 변수
    """
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
        gpt_client = ChatGPTClient()
        youtube_client = YoutubeClient()
        db_manager = DBManager()

        videos = youtube_client.request_video_info(broadcastID, maxResults)
            
        for video in videos:
            video_id = video["id"]
            actual_title = video["title"]
            thumbnail = video['thumbnail']
            transcript = youtube_client.request_transcript(video_id)

            summary = gpt_client.request_summary(transcript)
            title = gpt_client.request_title(summary)

            #DB에 뉴스 업데이트
            db_manager.insert_data(broadcastName, video_id, title, thumbnail, summary, actual_title)

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
        update.update_news('SBS', sbs_id, 30)
    

