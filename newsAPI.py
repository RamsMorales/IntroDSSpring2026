import requests
from dotenv import load_dotenv
import os

load_dotenv()

MYKEY = os.getenv("NEWS_API")
def get_articles(query):
    url = f"https://newsapi.org/v2/everything?q={query}&sortBy=popularity&apiKey={MYKEY}"

    response = requests.get(url).json()

    print(response.keys())
    print(response['status']) # this worked
    print(response['totalResults'])

    return response['status'], response['results']
#print(response['articles'])