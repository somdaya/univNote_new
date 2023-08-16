from flask import Flask, request
from Plus_Activity import Plus_Activity
from Search_Activity import Search_Activity
from Search_Club import Search_Club

from Search_Contest import Search_Contest

app = Flask(__name__)

@app.route("/contest/search/<keyword>", methods=['GET'])
def search_contest(keyword):
    idx = request.args.get('idx', default=0, type=int)
    data = Search_Contest(keyword=keyword, start_index=idx)
    return data;
  
@app.route("/activity/search/<keyword>", methods=['GET'])
def search_activity(keyword):
  idx = request.args.get('idx', default=0, type=int)
  data = Search_Activity(keyword=keyword, start_index=idx)
  return data;

@app.route("/club/search/<keyword>", methods=['GET'])
def search_club(keyword):
    idx = request.args.get('idx', default=0, type=int)
    data = Search_Club(keyword=keyword, start_index=idx)
    return data;

if __name__ == "__main__":
    app.run()