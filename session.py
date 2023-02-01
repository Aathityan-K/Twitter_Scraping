import streamlit as st
import snscrape.modules.twitter as sns
import pandas as pd
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient.twitter
mycol = mydb.tweets

st.sidebar.image(
    "https://static.vecteezy.com/system/resources/previews/000/066/728/original/vector-new-twitter-logo.jpg")
st.sidebar.title("Twitter Data")
key_word = st.sidebar.text_input("Enter Here To Search: ")
date_start = st.sidebar.date_input(" Select From Date: ")
date_end = st.sidebar.date_input("Select To Date: ")
length = st.sidebar.number_input("Enter The Range of Data You Need: ", 0, 1000, 1)
button = st.sidebar.button("Submit")
value = f'{key_word} since:{date_start} until:{date_end}'
title = f'Tweets for {key_word}'

tweets_list = []
if button:
    st.title(title)
    for i, tweet in enumerate(sns.TwitterSearchScraper(value).get_items()):
        if i > length:
            break
        tweets_list.append(
            [tweet.date, tweet.id, tweet.content, tweet.user.username, tweet.replyCount, tweet.retweetCount,
             tweet.likeCount, tweet.lang, tweet.source])  # declare the attributes to be returned

        st.write("User: ", tweet.username)
        st.write("Date: ", tweet.date)
        st.write("Tweet: ", tweet.content)
        st.write("Source: ", tweet.source)
        st.write("Likes: ", tweet.likeCount)
        st.write("Retweets: ", tweet.retweetCount)

        st.write("_" * 70)

    tweets_df = pd.DataFrame(tweets_list,
                             columns=['Datetime', 'Tweet Id', 'Text', 'Username', 'Replycount', 'Retweetcount',
                                      'Likecount', 'Language', 'Source'])


    def convert_df(a):
        records_ = tweets_df.to_dict(orient='records')
        return mycol.insert_many(records_)

    b = convert_df(tweets_df)

    st.write(tweets_df)

else:
    st.title("Twitter Scrapping")
    st.image("https://elearn.interviewgig.com/wp-content/uploads/2021/03/3331104_8292-2048x1152.jpg")
