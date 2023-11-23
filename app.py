from flask import Flask, render_template, request
from googleapiclient.discovery import build
#from googleapiclient.errors import HttpError
#import googleapiclient.discovery
from youtube_transcript_api import YouTubeTranscriptApi
from summary import ChatGPTClient

transcript_summarizer = ChatGPTClient()

app = Flask(__name__)
api_key = ""  # 여기에 유튜브 API 키를 삽입
youtube = build("youtube", "v3", developerKey=api_key)


def get_minute(str:str):
    str = str[2:]
    length = len(str)

    for i in range(length):
        if 'M' == str[i]:
            return int(str[:i])
        
    return 0
        
@app.route('/', methods=['GET', 'POST'])
def video_list():
    if request.method == 'POST':
        channel_id = request.form.get('channel_id')
    else:
        channel_id = "UCF4Wxdo3inmxP-Y59wXDsFw"
        
    videos = youtube.search().list(part="id", channelId=channel_id, maxResults=20, type="video", order = "date").execute()
    
    video_info = []
    for video in videos["items"]:
        video_id = video["id"]["videoId"]
        title = youtube.videos().list(part="snippet", id=video_id).execute()
        video_title = title["items"][0]["snippet"]["title"]
        video_thumbnail = title["items"][0]["snippet"]["thumbnails"]["default"]["url"]
        video_details = youtube.videos().list(part="contentDetails", id=video_id).execute()
        video_duration = video_details["items"][0]["contentDetails"]["duration"]

        if 'H' not in video_duration:
            minutes = get_minute(video_duration)
            if minutes <= 10:
                video_info.append({"id": video_id, "title": video_title, "thumbnail": video_thumbnail, "url": f"/play_video/{video_id}"})

    return render_template("videos.html", video_info=video_info)
    
@app.route('/play_video/<video_id>')
def play_video(video_id):
    print("Received Video ID:", video_id)
    
    transcript = ""
    try:
        tsAPI = YouTubeTranscriptApi.get_transcript(video_id=video_id, languages=["ko"])
        if "text" in tsAPI[0]:
            for dict in tsAPI:
                transcript += dict["text"]
        else:
            raise Exception("There is no Transcripts")
        
        summary = transcript_summarizer.request_summary(transcript)

    except Exception as e:
        print("Error:", str(e))
        summary = "Error occurred during transcript retrieval."
        
    print("Video ID:", video_id)

    return render_template('video_player.html', video_id=video_id, summary=summary)

if __name__ == '__main__':
    app.run()
