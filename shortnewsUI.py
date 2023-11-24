from flask import Flask, render_template, request, typing as ft
from flask.views import View
from manager import NewsManager

class ListView(View):
    methods=['GET', 'POST']

    def dispatch_request(self):
        newsManager = NewsManager()
        if request.method == 'POST':
            broadcastName = request.form.get('broadcastName')
        else:
            broadcastName = "MBC" #초기화면은 MBC로 설정
        video_info = newsManager.request_news(broadcastName)

        return render_template("videos.html", video_info=video_info)
    


class SummaryView(View):
    def request_summaryView(self, video_id):
        newsManager = NewsManager()
        summarized_news = newsManager.request_summary(video_id)
        video_id = summarized_news['video_id']
        summary = summarized_news['summary']
        
        return render_template('video_player.html', video_id=video_id, summary=summary)



app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def request_listView():
    newsManager = NewsManager()
    if request.method == 'POST':
        broadcastName = request.form.get('broadcastName')
    else:
        broadcastName = "MBC" #초기화면은 MBC로 설정
    video_info = newsManager.request_news(broadcastName)
        
    return render_template("videos.html", video_info=video_info)

@app.route('/play_video/<video_id>')
def request_summaryView(video_id):
    newsManager = NewsManager()
    summarized_news = newsManager.request_summary(video_id)
    video_id = summarized_news['video_id']
    summary = summarized_news['summary']
        
    return render_template('video_player.html', video_id=video_id, summary=summary)



"""
list_view = ListView()
summary_view = SummaryView()
app = Flask(__name__)
app.add_url_rule('/listview', view_func=list_view.as_view('listview'))
app.add_url_rule('/play_video/<video_id>', view_func=summary_view.as_view('summaryview'))

"""

if __name__ == '__main__':
    app.run()
