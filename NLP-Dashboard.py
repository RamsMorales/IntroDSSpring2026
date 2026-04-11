import streamlit as st
import time
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.probability import FreqDist
from nltk.sentiment import SentimentIntensityAnalyzer

import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

from wordcloud import WordCloud

import requests
from dotenv import load_dotenv
import os
import sys

from utils import on_select_change, on_text_change
#---------------------------------------------------------Startup-------------------------------------------------------------------------------

for pkg in ["punkt", "punkt_tab", "averaged_perceptron_tagger_eng", "vader_lexicon"]:
    try:
        nltk.download(pkg,quiet=True)
    except Exception:
        pass

POS_EXPLANATIONS = {
"CC": "Coordinating conjunction",
"CD": "Cardinal number",
"DT": "Determiner",
"EX": "Existential there",
"FW": "Foreign word",
"IN": "Preposition/subordinating conjunction",
"JJ": "Adjective",
"JJR": "Adjective, comparative",
"JJS": "Adjective, superlative",
"LS": "List item marker",
"MD": "Modal",
"NN": "Noun, singular or mass",
"NNS": "Noun, plural",
"NNP": "Proper noun, singular",
"NNPS": "Proper noun, plural",
"PDT": "Predeterminer",
"POS": "Possessive ending",
"PRP": "Personal pronoun",
"PRP$": "Possessive pronoun",
"RB": "Adverb",
"RBR": "Adverb, comparative",
"RBS": "Adverb, superlative",
"RP": "Particle",
"SYM": "Symbol",
"TO": "to",
"UH": "Interjection",
"VB": "Verb, base form",
"VBD": "Verb, past tense",
"VBG": "Verb, gerund/present participle",
"VBN": "Verb, past participle",
"VBP": "Verb, non-3rd person singular present",
"VBZ": "Verb, 3rd person singular present",
"WDT": "Wh-determiner",
"WP": "Wh-pronoun",
"WP$": "Possessive wh-pronoun",
"WRB": "Wh-adverb"
}

TOPICS = ["Technology","Science","Business","Health","Sports","Entertainment","Politics"]

load_dotenv()

api_key = os.getenv("NEWS_API")
#----------------------------------------------------------------------------------------------------------------------------------------

st.set_page_config(layout="wide")
if api_key is not None:
    #print("working!")
    st.title("News Dashboard")
    st.header("Spring 2026")
    st.subheader("Ramson Munoz Morales")
    st.divider()
    st.header("Choose your news!")
    container = st.container(border=True)
    with container:
        st.subheader("Select an area of interest or search a specific topic:")
        area = st.selectbox("General News Area:",TOPICS, index=None,key="search_category",on_change=on_select_change)
        topic = st.text_input("Enter a topic of interest:",max_chars=50,key="search_text",on_change=on_text_change)

        if area != None:
            query = area
            url = f"https://newsapi.org/v2/top-headlines?category={query}&sortBy=popularity&apiKey={api_key}"
        else:
            query = topic
            url = f"https://newsapi.org/v2/top-headlines?q={query}&sortBy=popularity&apiKey={api_key}"
        st.text(f"Your search term: {query}")
    st.divider()
    ready = st.button("Ready?")
    
    if ready:
        news_articles, metrics, reflection = st.tabs(["Aritlces","Metrics", "Reflection"]) 
        with news_articles:
            with st.spinner("Gathering articles"):
                time.sleep(2)
                try:
                    response = requests.get(url).json()
                except Exception :
                    st.error("Could not connect to API. Try again later")
                    st.stop()

                if response["status"] == "error":
                    st.warning("Your search result has an error. Try again!")
                    st.stop()
                elif response["totalResults"] == 0:
                    st.warning("No articles found for that search. Try again!")
                    st.stop()
                else:
                    st.header(f"Found {response["totalResults"]} articles!")
                    st.divider()
                    count = 0
                    max_articles = 10
                    st.subheader(f"Displaying top {max_articles} articles:")
                    st.divider()

                    articles_analysis_string = ""
                    for article in response["articles"]:
                        count += 1
                        st.subheader(article["title"])
                        st.write(article["description"])
                        st.write(article["source"]["name"])
                        if article["url"] is not None:
                            st.write(f"Visit the aritle here: {article["url"]}")
                        st.divider()
                        if count > max_articles:
                            break
                for article in response["articles"]:
                    if article["title"] is None:
                        st.warning("Missing title. Skipping article.")
                    elif article["description"] is None:
                        st.warning("Missing description. Skipping article.")
                    else:
                        articles_analysis_string += article["title"]
                        articles_analysis_string += article["description"]
        with metrics:
                #text preprocessing
                words = word_tokenize(articles_analysis_string)
                ## filter the words by checking if they are in the stopwords list and if they are alphabetic characters only
                filtered_words = []

                for i in words:
                    if i.lower() not in stopwords.words('english') and i.isalpha():
                        filtered_words.append(i.lower())
                
                # Getting word frequencies
                wordFreqMD = nltk.FreqDist(filtered_words)
                ## Visualising word frequencies
                mdDF = pd.DataFrame(wordFreqMD.most_common(20),columns=['Words','Counts'])
                st.subheader("Most common words")
                st.divider()
                
                chart, wordcloud = st.columns(2)
                st.dataframe(mdDF)
                with chart:
               # bar chart 
                    mdFig = px.bar(mdDF,x="Words",y="Counts")
                    st.plotly_chart(mdFig)
                with wordcloud:
                    # word cloud
                    with st.container(border=True): 
                        # creating word cloud
                        filteredMDText = ' '.join(filtered_words)
                        fig = WordCloud(width= 800, height=400, background_color='white').generate(filteredMDText)
                        fig_plot, ax = plt.subplots()
                        ax.imshow(fig, interpolation="bilinear")
                        ax.axis("off")
                        st.pyplot(fig_plot)
        with reflection:
            st.subheader("Reflection")
            st.write("My topic of search was 'Artificial Intelligence' because it seems appropriate given the context. The words that appeared most often were 'artificial', 'intelligence', 'ai', and 'bravo'. These are subject to change for the same search term since I am using the top stories api from newsAPI and sorting by popularity. The first three most frequent words make sense since they are key words related to the query, but bravo is a little puzzling due to my lack of knowledge of the business sphere of AI. The API did indeed reflect the topic I expected, but I tested the term 'ai' and received greater variation in the hits. It may be query dependent. For the broad category searches, greater variation is expected from my schema of what is relevant compared to the specific topic search method.")
                
else:
    sys.exit("Bad API Key") 

