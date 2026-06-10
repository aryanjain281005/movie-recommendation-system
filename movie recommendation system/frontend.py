import os
import streamlit as st
import pandas as pd
import pickle 

# Get path relative to the script directory to avoid FileNotFoundError
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, "data.pkl")
similarity_path = os.path.join(current_dir, "similarity.pkl")

st.title("Movie recommendation system")
data = pickle.load(open(data_path, "rb"))
# Reset the index to be contiguous so that DataFrame index labels align with similarity matrix positions
data.reset_index(drop=True, inplace=True)

cs = pickle.load(open(similarity_path, "rb"))


def reccomded(movie_name):
   
    i = data[data["title"] == movie_name].index[0]
    
    
    l = list(enumerate(cs[i]))
    n = sorted(l, key=lambda x: x[1], reverse=True)
    
    top_5_matches = n[1:6]

    recommend_list = []
    for match in top_5_matches:
        recommend_list.append(data.iloc[match[0]].title)
        
    return recommend_list


option = st.selectbox(
    "Select your movie",
    (data["title"].values),
)


if st.button("Give reccomedation", type="primary"):
    recommendations = reccomded(option)
    st.write("### Recommended Movies:")
    for movie in recommendations:
        st.write(movie)



