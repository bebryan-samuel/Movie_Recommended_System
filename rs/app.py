import  streamlit as st
import pickle 
import pandas as pd
import requests
import joblib

@st.cache_resource
def load_model():
    url = "https://drive.google.com/uc?export=download&id=1DWgq-6Yv7HwBCjucKkdnCCad9RC4VwCL"
    
    response = requests.get(url)
    
    # 🔥 check if download failed
    if response.status_code != 200:
        st.error("Failed to download model")
        return None

    # 🔥 write file properly
    with open("similarity.pkl", "wb") as f:
        f.write(response.content)

    # 🔥 DEBUG: check file size
    import os
    if os.path.getsize("similarity.pkl") < 1000000:
        st.error("Downloaded file is too small — likely wrong link")
        return None

    return joblib.load("similarity.pkl")

model = load_model()

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]

    recommend_movies = []
    for i in movies_list:
        recommend_movies.append(movies.iloc[i[0]].title)
    return recommend_movies

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

st.title("NXT Movie>>")
st.subheader("Movie Recommender System")

selected_movie_name = st.selectbox(
    "Recommend Movies",
    movies['title'].values
)

if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)
    for i in recommendations:
        st.write(i)