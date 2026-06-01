import streamlit as st
import pandas as pd
import pickle 

st.title("Movie recommendation system")
data = pickle.load(open("data.pkl", "rb"))
cs = pickle.load(open("similarity.pkl", "rb"))


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



