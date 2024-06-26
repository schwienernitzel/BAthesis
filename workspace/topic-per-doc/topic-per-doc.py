# @author: Felix Patryjas - https://github.com/schwienernitzel
# @date: 26-06-2024
# @title: Topic per Comment
# @version: v1.0

import sys

original_stdout = sys.stdout
topics_per_doc = topic_model.topics_

with open('output.txt', 'w', encoding='utf-8') as file:
    sys.stdout = file
    for i, comment in enumerate(comments):
        print(topics_per_doc[i], comment, sep='\t')
    sys.stdout = original_stdout

print("Done!")
