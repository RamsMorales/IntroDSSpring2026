import requests
from dotenv import load_dotenv
import os

load_dotenv()

MYKEY = os.getenv("NEWS_API")

url = f"https://newsapi.org/v2/everything?q=bitcoin&from=2026-01-03&sortBy=popularity&apiKey={MYKEY}"

response = requests.get(url).json()

print(response.keys())
print(response['status']) # this worked
print(response['totalResults'])
#print(response['articles'])