import pandas as pd
import matplotlib.pyplot as plt

csv_file = 'out/raw-4.csv'  # Passe den Pfad entsprechend an

df = pd.read_csv(csv_file, delimiter='\t')
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year

comments_per_year = df.groupby('year').size()
total_comments = comments_per_year.sum()
plt.figure(figsize=(10, 6))
bars = plt.bar(comments_per_year.index, comments_per_year.values, color='skyblue')

for bar, count in zip(bars, comments_per_year.values):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(), count,
             ha='center', va='bottom', fontsize=10)

plt.title(f'Verteilung der YouTube-Kommentare in Abhängigkeit des Jahres (Gesamt: {total_comments})')
plt.xlabel('Jahr')
plt.ylabel('Anzahl der Kommentare')
plt.xticks(comments_per_year.index, rotation=45, ha='right')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()