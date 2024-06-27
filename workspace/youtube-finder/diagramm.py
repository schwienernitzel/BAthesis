import matplotlib.pyplot as plt

dateipfad = 'out/videolist-20240626-0849.txt'
video_ids_pro_jahr = {}
jahr_muster = '# '

with open(dateipfad, 'r') as file:
    current_year = None
    for line in file:
        line = line.strip()
        if line.startswith(jahr_muster):
            current_year = line.replace(jahr_muster, '')
            if current_year not in video_ids_pro_jahr:
                video_ids_pro_jahr[current_year] = 0
        elif line != '':
            if current_year:
                video_ids_pro_jahr[current_year] += 1

jahre = list(video_ids_pro_jahr.keys())
anzahlen = list(video_ids_pro_jahr.values())
gesamt_anzahl = sum(anzahlen)

plt.figure(figsize=(10, 6))
plt.bar(jahre, anzahlen, color='skyblue')
plt.xlabel('Jahr')
plt.ylabel('Anzahl der Videos')
plt.title(f'Verteilung der YouTube-Videos in Abhängigkeit des Jahres (Gesamt: {gesamt_anzahl})')
plt.xticks(rotation=45)

for i, anzahl in enumerate(anzahlen):
    plt.text(i, anzahl + 0.2, str(anzahl), ha='center', va='bottom')

plt.text(len(jahre)-0.5, max(anzahlen), f'Gesamt: {gesamt_anzahl}', fontsize=10, ha='right', va='top')
plt.tight_layout()
plt.show()