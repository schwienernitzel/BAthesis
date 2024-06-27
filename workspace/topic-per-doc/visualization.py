import numpy as np
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

filename = 'out/output.txt'
documents = []
topics_per_doc = []

with open(filename, 'r', encoding='utf-8') as file:
    for line in file:
        topic, comment = line.strip().split('\t')
        topics_per_doc.append(int(topic))
        documents.append(comment)

topics_per_doc = np.array(topics_per_doc)

num_docs = len(topics_per_doc)
num_topics = len(set(topics_per_doc))
topic_embeddings = np.zeros((num_docs, num_topics))

for i, topic in enumerate(topics_per_doc):
    topic_embeddings[i, topic] = 1

tsne = TSNE(n_components=2, random_state=42, perplexity=5)
tsne_results = tsne.fit_transform(topic_embeddings)

num_clusters = len(set(topics_per_doc))
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
clusters = kmeans.fit_predict(tsne_results)

topic_descriptions = [
    "Talkshow",
    "Politik",
    "Deutschland",
    "Migration",
    "Islam",
    "Videos",
    "Parteien"
    "Scholz",
    "Kommentare",
    "Datenschutz",
    "Asien",
    "Integration",
]

plt.figure(figsize=(12, 8))
scatter = plt.scatter(tsne_results[:, 0], tsne_results[:, 1], c=clusters, cmap='viridis', alpha=0.5)
plt.colorbar(scatter, label='Cluster')
plt.xlabel('TSNE Dimension 1')
plt.ylabel('TSNE Dimension 2')
plt.title('TSNE Visualization with K-Means Clustering')

cluster_centers = kmeans.cluster_centers_

tsne_cluster_centers = TSNE(n_components=2, random_state=42, perplexity=2).fit_transform(cluster_centers)

for i, (x, y) in enumerate(tsne_cluster_centers):
    plt.text(x, y, topic_descriptions[i] if i < len(topic_descriptions) else f'Cluster {i}', fontsize=12, ha='center', va='center',
             bbox=dict(facecolor='white', alpha=0.6, edgecolor='black', boxstyle='round,pad=0.5'))
plt.show()