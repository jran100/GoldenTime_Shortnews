from flask import Flask, render_template, request
from flask.views import View

from manager import NewsManager


#TODO(백정란): ListView 클래스 기반 뷰에 대해 오류를 해결 한 후, ListView 관련 주석 해제
#TODO(윤성원): SummaryView 클래스 기반 뷰에 대해 오류를 해결 한 후, SummaryView 관련 주석 해제

"""

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

list_view = ListView()
summary_view = SummaryView()
app = Flask(__name__)
app.add_url_rule('/listview', view_func=list_view.as_view('listview'))
app.add_url_rule('/play_video/<video_id>', view_func=summary_view.as_view('summaryview'))



if __name__ == '__main__':
    app.run()


"""


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


if __name__ == '__main__':
    app.run()
