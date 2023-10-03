import googleapiclient.discovery
from youtube_transcript_api import YouTubeTranscriptApi

def get_minute(str:str):
    '''
    PT분M초S 형식으로 된 duration에 대해 분 단위로 출력하는 함수
    '''
    str = str[2:]
    length = len(str)

    for i in range(length):
        if 'M' == str[i]:
            return int(str[:i])
            
    return 0

def get_video_transcript(video_id):
    '''
    video id를 바탕으로 해당 동영상의 자막을 가져오는 함수
    '''
    try:
        tsAPI = YouTubeTranscriptApi.get_transcript(video_id=video_id, languages=["ko"])
        if "text" in tsAPI[0]:
            for object in tsAPI:
                print(object["text"])
        else:
            raise Exception("There is no Transcripts")

    except Exception as e:
        print("Error:", str(e))

    return

# API 키 설정
api_key = "api-key"

# YouTube API 클라이언트 생성
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

channel_id = "UCF4Wxdo3inmxP-Y59wXDsFw"
videos = youtube.search().list(part="id", channelId=channel_id, maxResults=1, type="video", order="date").execute()

for video in videos["items"]:
    video_id = video["id"]["videoId"]
    title = youtube.videos().list(part="snippet", id=video_id).execute()

    video_details = youtube.videos().list(part="contentDetails", id=video_id).execute()
    video_duration = video_details["items"][0]["contentDetails"]["duration"]

    if 'H' not in video_duration:
        print(title["items"][0]["snippet"]["title"])
        print(get_minute(video_duration))
        get_video_transcript(video_id)
        print()
