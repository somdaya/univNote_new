from fastapi import FastAPI
from best.best_activity import best_activity
from best.best_club import best_club
from best.best_contest import best_contest
from filed_class import activity_contest_result, close_major, get_matching_activities
from plus.plus_activity import plus_activity
from plus.plus_club import plus_club
from plus.plus_contest import plus_contest

from review import review

app = FastAPI()

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
def show_best_contest():
    data = best_contest()
    return data;

@app.get("/activity/best")
def show_best_activity():
    data = best_activity()
    return data;

@app.get("/club/best")
def show_best_club():
    data = best_club()
    return data;

@app.get("/reviews")
def show_reviews(keyword: str):
    data = review(keyword)
    return data;

@app.get("/recommend")
def show_matching_activities(major: str):
    activity_contest_results = activity_contest_result()
    random_matching_activities = get_matching_activities(activity_contest_results, close_major(major))
    
    return random_matching_activities

if __name__ == "__main__":
    app.run()