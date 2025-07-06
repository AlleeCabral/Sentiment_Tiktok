#!/usr/bin/env python3
#!/home/alex/UE-Germany/ps25_bigdata/Sentiment_Tiktok/.venv/bin/python

import nltk
nltk.download('stopwords')
import sys
import json
import re
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^\w\s]", "", text)
    return [word for word in text.split() if word not in stop_words]

def process(record):
    if 'body' in record and isinstance(record['body'], str):
        words = clean_text(record['body'])
        for word in words:
            print(f"{word}\t1")

try:
    content = sys.stdin.read()
    data = json.loads(content)
    if isinstance(data, list):
        for record in data:
            process(record)
    else:
        process(data)
except Exception:
    # This script is called "mapperflatter" because it not only maps over each object in the input array (processing each record individually),
    # but also "flattens" the structure by emitting each word from the 'body' field as a separate output line.
    # This flattening transforms nested or grouped data into a simple, line-by-line format suitable for further processing in data pipelines.
    pass