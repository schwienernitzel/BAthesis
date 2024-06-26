# @author: Felix Patryjas - https://github.com/schwienernitzel
# @date: 26-06-2024
# @title: Seperate Topic Modelling which is needed before running 'Topic per Comments'
# @version: v1.0

from bertopic import BERTopic
import re
import pandas as pd
import nltk

nltk.download('stopwords')
from nltk.corpus import stopwords

filename = 'raw-4.csv'

comments = []
with open(filename, "r") as file_content:
    for line in file_content.readlines():
        line = line.strip()
        line = re.sub('[\s]+', ' ', line)
        line = line.lower()
        line = re.sub('[^a-zäöüß -]', '', line)
        comments.append(line)

comments_without_stopwords = []
for comment in comments:
    word_list = comment.split(' ')
    filtered_words = [word for word in word_list if word not in stopwords.words('german')]
    filtered_words = [word for word in filtered_words if word not in stopwords.words('english')]
    new_comment = ' '.join(filtered_words)
    comments_without_stopwords.append(new_comment)
comments = comments_without_stopwords

topic_model = BERTopic(language="multilingual", nr_topics=20)
topics, probs = topic_model.fit_transform(comments)

topic_model.visualize_barchart(top_n_topics=12, n_words=8)
