from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build

api_key = "AIzaSyCcu40FYJarmjUNyilOh4gLPab8DSEOeno"  # 여기에 유튜브 API 키를 삽입


class YoutubeClient():
    def __init__(self, broadcastID):
        self.youtube = build("youtube", "v3", developerKey=api_key)
        self.broadcaseID = broadcastID #channel id of youtube channel

    def request_transcript(self, videoID) -> str:
        '''
        video id를 바탕으로 해당 동영상의 자막을 가져오는 함수
        '''
        transcript = ""
        try:
            tsAPI = YouTubeTranscriptApi.get_transcript(video_id=videoID, languages=["ko"])
            if "text" in tsAPI[0]:
                for dict in tsAPI:
                    transcript += dict["text"]
            else:
                raise Exception("There is no Transcripts")

        except Exception as e:
            print("Error:", str(e))

        return transcript
    
    def request_video_length(self, videoID:str):
        '''
        영상 길이를 가져오는 함수
        *00H00M 형식
        '''
        video_details = self.youtube.videos().list(part="contentDetails", id=videoID).execute()
        video_duration = video_details["items"][0]["contentDetails"]["duration"]
        
        return video_duration
    

    def request_video_info(self, maxResults) -> list:
        video_info = []
        videos = self.youtube.search().list(part="id",
                                            channelId=self.broadcaseID,
                                            maxResults=maxResults,
                                            type="video", order = "date").execute()
        for video in videos["items"]:
            video_id = video["id"]["videoId"]
            title = self.youtube.videos().list(part="snippet", id=video_id).execute()
            video_title = title["items"][0]["snippet"]["title"]
            video_thumbnail = title["items"][0]["snippet"]["thumbnails"]["default"]["url"]

            video_duration = self.request_video_length(video_id)

            if 'H' not in video_duration:
                minutes = self.get_minute(video_duration)
                if minutes <= 10 and minutes > 2:
                    video_info.append({"id": video_id, "title": video_title, "thumbnail": video_thumbnail, "url": f"/play_video/{video_id}"})

        return video_info
    
    def get_minute(self, str:str) -> int:
        str = str[2:]
        length = len(str)

        for i in range(length):
            if 'M' == str[i]:
                return int(str[:i])
        
        return 0

