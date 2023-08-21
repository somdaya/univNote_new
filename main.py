from fastapi import FastAPI
from Like_Activity import like_activity
from Like_Club import like_club
from Like_Contest import like_contest
from Plus_Activity import plus_activity
from Plus_Club import plus_club
from Plus_Contest import plus_contest

from Search_Activity import search_activity
from Search_Club import search_club
from Search_Contest import search_contest
from review import review

app = FastAPI()

@app.get("/contest/search/{keyword}")
def search_contents(keyword: str, idx: int = 0):
    data = search_contest(keyword=keyword, start_index=idx)
    return data;
  
@app.get("/activity/search/{keyword}")
def search_activities(keyword: str, idx: int = 0):
  data = search_activity(keyword=keyword, start_index=idx)
  return data;

@app.get("/club/search/{keyword}")
def search_clubs(keyword: str, idx: int = 0):
    data = search_club(keyword=keyword, start_index=idx)
    return data;

@app.get("/contest")
def show_all_contest(idx: int = 0):
    data = plus_contest(start_index=idx)
    return data;

@app.get("/activity")
def show_all_activity(idx: int = 0):
    data = plus_activity(start_index=idx)
    return data;

@app.get("/club")
def show_all_club(idx: int = 0):
    data = plus_club(start_index=idx)
    return data;

@app.get("/contest/best")
def best_contest():
    data = like_contest()
    return data;

@app.get("/activity/best")
def best_activity():
    data = like_activity()
    return data;

@app.get("/club/best")
def best_club():
    data = like_club()
    return data;

@app.get("/reviews/{keyword}")
def show_reviews(keyword: str):
    data = review(keyword)
    return data;

if __name__ == "__main__":
    app.run()