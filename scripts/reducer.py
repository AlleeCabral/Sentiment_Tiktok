#!/usr/bin/env python3
#!/home/alex/UE-Germany/ps25_bigdata/Sentiment_Tiktok/.venv/bin/python

import sys

current_word = None
current_count = 0

for line in sys.stdin:
    word, count = line.strip().split('\t')
    count = int(count)
    
    if word == current_word:
        current_count += count
    else:
        if current_word is not None:
            print(f"{current_word}\t{current_count}")
        current_word = word
        current_count = count

# Don't forget the last word
if current_word is not None:
    print(f"{current_word}\t{current_count}")
