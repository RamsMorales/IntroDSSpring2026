import nltk
from nltk.corpus import stopwords, gutenberg
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt

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
print(filterered_message)

# Creating a word cloud to visualize the most common words in the filtered message
from wordcloud import WordCloud
fig = WordCloud(width= 800, height=400, background_color='white').generate(filterered_message)

plt.figure(figsize=(10,7))
plt.imshow(fig)
plt.axis('off')
plt.show()