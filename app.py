from flask import Flask, render_template
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

app = Flask(__name__)

# YouTube API 키 설정
api_key = "AIzaSyCcu40FYJarmjUNyilOh4gLPab8DSEOeno"  # 여기에 유튜브 API 키를 삽입

# YouTube API 클라이언트 생성
youtube = build("youtube", "v3", developerKey=api_key)

# 뷰 함수: 비디오 목록을 가져와 템플릿에 전달
@app.route('/')
def video_list():
    channel_id = "UCF4Wxdo3inmxP-Y59wXDsFw"  # MBC 뉴스 채널 ID
    videos = youtube.search().list(part="id", channelId=channel_id, maxResults=10, type="video").execute()
    
    video_info = []
    for video in videos["items"]:
        video_id = video["id"]["videoId"]
        title = youtube.videos().list(part="snippet", id=video_id).execute()
        video_title = title["items"][0]["snippet"]["title"]
        video_thumbnail = title["items"][0]["snippet"]["thumbnails"]["default"]["url"]
        video_info.append({"id": video_id, "title": video_title, "thumbnail": video_thumbnail})
    
    return render_template('videos.html', video_info=video_info)

if __name__ == '__main__':
    app.run()
