import nltk
from nltk.corpus import stopwords, gutenberg
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
import plotly.express as px

### gutenberg is a collection of free use books as expected, a dataset


text = """You don’t get better on the days when you feel like going. You get better on the days when you don’t want to go, but you go anyway. If you can overcome the negative energy coming from your tired body or unmotivated mind, you will grow and become better. It won’t be the best workout you have, you won’t accomplish as much as what you usually do when you actually feel good, but that doesn’t matter. Growth is a long term game, and the crappy days are more important."""


#nltk.download('stopwords')
#nltk.download('punkt_tab')
#nltk.download('averaged_perceptron_tagger_eng')

words = word_tokenize(text)
#print(words)


## filter the words by checking if they are in the stopwords list and if they are alphabetic characters only
filtered_words = []

for i in words:
    if i.lower() not in stopwords.words('english') and i.isalpha():
        filtered_words.append(i)

#print(filtered_words)

# Transforming the list to a string

filterered_message = ' '.join(filtered_words)
#print(filterered_message)

# Creating a word cloud to visualize the most common words in the filtered message
from wordcloud import WordCloud
fig = WordCloud(width= 800, height=400, background_color='white').generate(filterered_message)

plt.figure(figsize=(10,7))
#plt.imshow(fig)
plt.axis('off')
#plt.show()

## finding freq dist of the words
word_frequencies = nltk.FreqDist(filtered_words)
#print(word_frequencies.most_common(10))

#creating a dataframe to visulize the distribution of the most common words
import pandas as pd

df = pd.DataFrame(word_frequencies.most_common(10), columns=['Word', 'Count'])

fig = px.bar(df,x="Word",y="Count",title="Top 10 word Counts")
#fig.show()

## Example 2 using the gutenberg dataset

#nltk.download('gutenberg')

#print(gutenberg.fileids())


# extracting raw text
ebook_melville = gutenberg.raw('melville-moby_dick.txt')

# tokenizing text
wordsMD = word_tokenize(ebook_melville)

# filtering for stop words
filteredMD = []
for word in wordsMD:
    if word.lower() not in stopwords.words('english') and word.isalpha():
        filteredMD.append(word)

# creating word cloud
filteredMDText = ' '.join(filteredMD)
fig = WordCloud(width= 800, height=400, background_color='white').generate(filteredMDText)

plt.imshow(fig)
plt.show()

# Getting word frequencies
wordFreqMD = nltk.FreqDist(filteredMD)

## Visualising word frequencies
mdDF = pd.DataFrame(wordFreqMD.most_common(50),columns=['Words','Counts'])

mdFig = px.bar(mdDF,x="Words",y="Counts")
mdFig.show()

from nltk.sentiment import vader
#nltk.download('vader_lexicon')

watchDog = vader.SentimentIntensityAnalyzer()

scores = watchDog.polarity_scores("I hate hate. Hate is hateful. Don't be hateful. Be glad")
print(scores)