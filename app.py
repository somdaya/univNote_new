from flask import Flask, request

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

if __name__ == "__main__":
    app.run()