# !pip install transformers

use_cuda=True

from transformers import pipeline
from time import sleep
import re

print("Setting up variables...")
filename = '../youtube-scraper/out/raw-3.csv'
pipe = pipeline("text-classification", model="deepset/bert-base-german-cased-hatespeech-GermEval18Coarse")
model="deepset/bert-base-german-cased-hatespeech-GermEval18Coarse"
content = []
print("Done!")

print("Load output file...")
with open(filename, "r") as file_content:
    for line in file_content.readlines():
        line = re.sub('[\s]+', ' ', line)
        if not re.search('[a-zA-z]', line) or len(line) < 10:
            continue
        line = line.strip()
        content.append(line)
print("Done!")

print("Loading the text-classification model...")
pipe = pipeline("text-classification", model="deepset/bert-base-german-cased-hatespeech-GermEval18Coarse")
string_to_file = ''
print(f"Done! Using the model: {model}")

print("Classifying hate-speech in the current data set...")
for line in content:
    try:
        out = pipe(line)
        label = re.sub('.*\'([A-Z]+).*', r'\1', str(out))
        score = re.sub('.*score\': ([\d\.]+).*', r'\1', str(out))
        string_to_file += label+'\t'+score+'\t'+line+'\n' 
    except:
        continue
print("Done!")

print("Writing output file...")
string_to_file = string_to_file.strip()
with open('/content/hatespeech.csv', 'w') as writefile:
    writefile.write(string_to_file)
print("Done! File saved as 'hatespeech.csv'.")
