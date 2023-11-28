from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build
import openai


class ChatGPTClient():
    """
    Chat GPT API를 통해 GPT에게 요약을 요청하는 메소드를 가지고 있다.

    Attributes:
        openai: openai 객체
        openai.api: 문자열 형태의 api key를 저장하는 멤버 변수
    """
    def __init__(self) -> None:
        self.openai = openai
        self.openai.api_key = "api-key"

    def request_summary(self, transcript) -> str:
        messages = []
        content = "다음 뉴스 스크립트를 5개의 문장으로 요약해줘\n 뉴스 스크립트:\n" + transcript
        messages.append({"role": "user", "content": f"{content}"})

        response = self.openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=messages
        )
        return response['choices'][0]['message']['content'].strip()
    
    def request_title(self, summary) -> str:
        messages = []
        content = "다음 뉴스 요약본을 1개의 제목으로 만들어줘\n 뉴스 요약본:\n" + summary
        messages.append({"role": "user", "content": f"{content}"})

        response = self.openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=messages
        )
        return response['choices'][0]['message']['content'].strip()


class YoutubeClient():
    """
    Youtube API를 통해 유튜브로부터 제목, 썸네일, 자막등을 가져오는 메소드를 가지고 있다.

    Attributes:
        youtube: channel_id, video_id 등의 값으로 해당 채널의 영상 정보를 가져오는 객체를 저장
    """
    def __init__(self):
        self.youtube = build(
            "youtube",
            "v3",
            developerKey="AIzaSyCcu40FYJarmjUNyilOh4gLPab8DSEOeno")

    def request_transcript(self, video_id) -> str:
        transcript = ""
        try:
            tsAPI = YouTubeTranscriptApi.get_transcript(video_id=video_id, languages=["ko"])
            if "text" in tsAPI[0]:
                for dict in tsAPI:
                    transcript += dict["text"]
            else:
                raise Exception("There is no Transcripts")

        except Exception as e:
            print("Transcript API Error:", str(e))

        return transcript
    
    def request_video_length(self, videoID) -> str:
        '''
        영상 길이를 가져오는 함수
        return: 'T00H00M' 문자열 형식
        '''
        video_details = self.youtube.videos().list(part="contentDetails", id=videoID).execute()
        video_duration = video_details["items"][0]["contentDetails"]["duration"]
        
        return video_duration
    

    def request_video_info(self, broadcastID, maxResults) -> list:
        video_info = []
        videos = self.youtube.search().list(part="id",
                                            channelId=broadcastID,
                                            maxResults=maxResults,
                                            type="video", order = "date").execute()
        for video in videos["items"]:
            video_id = video["id"]["videoId"]
            title = self.youtube.videos().list(part="snippet", id=video_id).execute()
            video_title = title["items"][0]["snippet"]["title"]
            video_thumbnail = title["items"][0]["snippet"]["thumbnails"]["standard"]["url"]

            video_duration = self.request_video_length(video_id)

            if 'H' not in video_duration:
                minutes = self.get_minute(video_duration)
                if minutes <= 10 and minutes > 1:
                    video_info.append({"id": video_id,
                                       "title": video_title,
                                       "thumbnail": video_thumbnail,
                                       "url": f"/play_video/{video_id}"})

        return video_info
    
    def get_minute(self, str:str) -> int:
        str = str[2:]
        length = len(str)

        for i in range(length):
            if 'M' == str[i]:
                return int(str[:i])
        
        return 0