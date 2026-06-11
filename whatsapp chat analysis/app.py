import streamlit as st
import dataframe_maker


st.sidebar.title("WHATSAPP CHAT ANALYSER")

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = dataframe_maker.parse_whatsapp_chat(data)

    userlist = df["Sender"].unique().tolist()
    if "System" in userlist:
        userlist.remove("System")
    userlist.sort()
    userlist.insert(0, "overall")
    
    selected_user = st.sidebar.selectbox("Show Analysis For", userlist)

    if selected_user != "overall":
        df = df[df["Sender"] == selected_user]
    button = st.sidebar.button("show analaysis")
    st.dataframe(df)