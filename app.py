from flask import Flask, request
from Plus_Activity import plus_activity
from Plus_Club import plus_club
from Plus_Contest import plus_contest

from Search_Activity import search_activity
from Search_Club import search_club
from Search_Contest import search_contest

app = Flask(__name__)

@app.route("/contest/search/<keyword>", methods=['GET'])
def search_contents(keyword):
    idx = request.args.get('idx', default=0, type=int)
    data = search_contest(keyword=keyword, start_index=idx)
    return data;
  
@app.route("/activity/search/<keyword>", methods=['GET'])
def search_activities(keyword):
  idx = request.args.get('idx', default=0, type=int)
  data = search_activity(keyword=keyword, start_index=idx)
  return data;

@app.route("/club/search/<keyword>", methods=['GET'])
def search_clubs(keyword):
    idx = request.args.get('idx', default=0, type=int)
    data = search_club(keyword=keyword, start_index=idx)
    return data;

@app.route("/contest", methods=['GET'])
def show_all_contest():
    idx = request.args.get('idx', default=0, type=int)
    data = plus_contest(start_index=idx)
    return data;

@app.route("/activity", methods=['GET'])
def show_all_activity():
    idx = request.args.get('idx', default=0, type=int)
    data = plus_activity(start_index=idx)
    return data;

@app.route("/club", methods=['GET'])
def show_all_club():
    idx = request.args.get('idx', default=0, type=int)
    data = plus_club(start_index=idx)
    return data;

if __name__ == "__main__":
    app.run()