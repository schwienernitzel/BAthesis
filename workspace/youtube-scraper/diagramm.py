import pandas as pd
import matplotlib.pyplot as plt

# Dateipfad zur CSV-Datei
csv_file = 'out/raw-4.csv'  # Passe den Pfad entsprechend an

# CSV-Datei einlesen
df = pd.read_csv(csv_file, delimiter='\t')

# Konvertiere das 'date' Feld in ein datetime-Objekt
df['date'] = pd.to_datetime(df['date'])

# Extrahiere das Jahr aus dem Datum
df['year'] = df['date'].dt.year

# Gruppiere nach Jahr und zähle die Anzahl der Kommentare
comments_per_year = df.groupby('year').size()

# Balkendiagramm erstellen
plt.figure(figsize=(10, 6))
bars = plt.bar(comments_per_year.index, comments_per_year.values, color='skyblue')

# Texte über den Balken platzieren
for bar, count in zip(bars, comments_per_year.values):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(), count,
             ha='center', va='bottom', fontsize=10)

plt.title('Anzahl der YouTube-Kommentare pro Jahr')
plt.xlabel('Jahr')
plt.ylabel('Anzahl der Kommentare')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Diagramm anzeigen
plt.show()