from flask import Flask, render_template, request
from manager import NewsManager


app = Flask(__name__)

class ListView():
    def __init__(self):
        self.newsManager = NewsManager()

    def request_listView(self):
        video_info = self.newsManager.request_news()

        
        return render_template("videos.html", video_info=video_info)



class SummaryView():
    def __init__(self):
        self.newsManager = NewsManager()

    def request_summaryView(self, video_id):
        video_id = request.args.get('video_id')
        summarized_news = self.newsManager.request_summary(video_id)
        video_title = summarized_news['video_title']
        summary = summarized_news['summary']
        
        return render_template('video_player.html', video_id=video_id, video_title=video_title, summary=summary)


newsManager = NewsManager()
li = newsManager.request_news('MBC')

for i in li:
    print(i['video_id'])
    print(i['title'])
    print(i['thumbnail'])
