from flask import Flask, jsonify, request
from demographic_filtering import output
from content_filtering import get_recommendations
import pandas as pd

movies_data = pd.read_csv('final.csv')

app = Flask(__name__)

all_movies = movies_data[["original_title","poster_link","release_date","runtime","weighted_rating"]]

liked_movies = []
not_liked_movies = []
did_not_watch = []

def assign_val():
    m_data = {
        "original_title": all_movies.iloc[0,0],
        "poster_link": all_movies.iloc[0,1],
        "release_date": all_movies.iloc[0,2] or "N/A",
        "duration": all_movies.iloc[0,3],
        "rating":all_movies.iloc[0,4]/2
    }
    return m_data

@app.route("/movies")
def get_movie():
    movie_data = assign_val()

    return jsonify({
        "data": movie_data,
        "status": "success"
    })

@app.route("/like")
def liked_movie():
    global all_movies
    movie_data=assign_val()
    liked_movies.append(movie_data)
    all_movies.drop([0], inplace=True)
    all_movies = all_movies.reset_index(drop=True)
    return jsonify({
        "status": "success"
    })

# api to return list of liked movies



@app.route("/dislike")
def unliked_movie():
    global all_movies

    movie_data=assign_val()
    not_liked_movies.append(movie_data)
    all_movies.drop([0], inplace=True)
    all_movies=all_movies.reset_index(drop=True)
    
    return jsonify({
        "status": "success"
    })

@app.route("/did_not_watch")
def did_not_watch_view():
    global all_movies

    movie_data=assign_val()
    did_not_watch.append(movie_data)
    all_movies.drop([0], inplace=True)
    all_movies=all_movies.reset_index(drop=True)
    
    return jsonify({
        "status": "success"
    })

# api to return list of popular movies
@app.route("/popularmovies")
def popular_movies():
    popular_movies=[]
    for i,row in output.iterrows():
          n_data = {
        "original_title": row["orginal_title"],
        "poster_link": row["poster_links"],
        "release_date": row["release_date"] or "NA",
        "duration": row["runtime"],
        "rating":row["weighted_rating"],

    }
    popular_movies.append(n_data)
    return jsonify({
        "status":"sucess",
        "data": popular_movies
    })



# api to return list of recommended movies
@app.route("/recommendedmovies")
def recommendedmovies():
    global liked_movies
    colomnnames=['original_title' , 'poster_link' , 'runtime', 'release_date' , 'weighted_rating']
    recommendations=pd.DataFrame(columns=colomnnames)
    for i in liked_movies:
        output1=get_recommendations(liked_movie["orginal_title"])
        recommendations=recommendations.append(output1)
    recommendations.drop_duplicates(subset=["orginal_title"],inplace=True)
    recommendedmovies=[]
    for i,row in recommendations.iterrows():
          n_data = {
        "original_title": row["orginal_title"],
        "poster_link": row["poster_links"],
        "release_date": row["release_date"] or "NA",
        "duration": row["runtime"],
        "rating":row["weighted_rating"],
        }
    recommendedmovies.append(n_data)
    return jsonify()({
        "status":"sucess",
        "data":recommendedmovies
    })






if __name__ == "__main__":
  app.run()
#upgrade sklearn -m