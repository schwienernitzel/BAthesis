# To make this script work, run '!pip install bertopic' before
from bertopic import BERTopic
import re
import pandas as pd
import nltk

nltk.download('stopwords')
from nltk.corpus import stopwords

filename = 'sample_data/migration-test.csv' # Insert your own filepath

content = ' '
with open(filename, "r") as file_content:
    for line in file_content.readlines():
        line = line.strip()
        line = re.sub('[\s]+', ' ', line)
        line = line.lower()
        line = re.sub('[^a-zäöüß0-9 -]', '', line)
        content += ' '+line
content = re.sub('[\s]+', ' ', content)
content = content.strip()

n = 50

parts = [''.join(content[i:i+n]) for i in range(0,len(content),n)]
new_parts = []
for part in parts:
    word_list = part.split(' ')
    filtered_words = [word for word in word_list if word not in stopwords.words('german')]
    filtered_words = [word for word in filtered_words if word not in stopwords.words('english')]
    new_content = ' '.join(filtered_words)
    new_parts.append(new_content)
parts = new_parts

topic_model = BERTopic(language="multilingual", nr_topics=20)
topics, probs = topic_model.fit_transform(parts)
topic_model.visualize_barchart(top_n_topics=10, n_words=10) # Adjust number of topics and keywords