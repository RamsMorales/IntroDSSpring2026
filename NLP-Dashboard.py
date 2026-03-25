import streamlit as st

import nltk
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


if api_key is not None:
    #print("working!")
    st.title("News Dashboard")
    st.header("Spring 2026")
    st.subheader("Ramson Munoz Morales")
    st.divider()
    st.header("Choose your news!")
    container = st.container(border=True)
    with container:
        area = st.selectbox("General News Area:",TOPICS)
        topic = st.text_input("Enter a topic of interest:",max_chars=50)

        query = ""

        queryLogic = st.selectbox("Search Logic:",["Combined","Separate"])

        if queryLogic == "Combined":
            combLogic = st.selectbox("Combination Logic:",["AND", "OR"])
            query = area + combLogic + topic

        elif queryLogic == "Separate":
            query = st.selectbox("Search Area or topic:",[area,topic])


        st.text(f"Your search term: {query}")
    st.divider()


else:
    sys.exit("Bad API Key") 


