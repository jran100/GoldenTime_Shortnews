from flask import Flask
from shortnewsUI import ListView
from shortnewsUI import SummaryView



app = Flask(__name__)

list_view = ListView()
summary_view = SummaryView()

app.add_url_rule('/', view_func=list_view.request_listView())
app.add_url_rule('/play_video/<video_id>', view_func=summary_view.request_summaryView())


