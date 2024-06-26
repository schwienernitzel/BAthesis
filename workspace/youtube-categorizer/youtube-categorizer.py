import pandas as pd
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
nltk.download('stopwords')

# Einlesen der Daten aus der CSV-Datei
file_path = '../youtube-scraper/out/raw-4.csv'
df = pd.read_csv(file_path, sep='\t')  # Angenommen, deine Daten sind tab-separiert

# Vorbereitung der Kommentare
comments = df['comment'].astype(str)

# German stopwords
german_stopwords = set(stopwords.words('german'))
stop_words_list = list(german_stopwords)

# TF-IDF Vektorisierung der Kommentare
vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, stop_words=stop_words_list)
tfidf = vectorizer.fit_transform(comments)

# LDA Modell für Topic Modeling
num_topics = 5  # Anzahl der zu identifizierenden Themen
lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
lda.fit(tfidf)

# Top Wörter pro Thema ausgeben
feature_names = vectorizer.get_feature_names_out()
for topic_idx, topic in enumerate(lda.components_):
    print(f"Topic {topic_idx + 1}:")
    print([feature_names[i] for i in topic.argsort()[:-10 - 1:-1]])
    print()

# Zuordnung der Kommentare zu Themen
topic_predictions = lda.transform(tfidf)
df['topic'] = topic_predictions.argmax(axis=1)

# Visualisierung der Themenverteilung
topic_counts = df['topic'].value_counts()
plt.figure(figsize=(8, 5))
topic_counts.sort_index().plot(kind='bar')
plt.xlabel('Thema')
plt.ylabel('Anzahl der Kommentare')
plt.title('Verteilung der Themen in den Kommentaren')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()