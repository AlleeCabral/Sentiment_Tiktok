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

for line in sys.stdin:
    try:
        record = json.loads(line)
        if 'body' in record and isinstance(record['body'], str):
            words = clean_text(record['body'])
            for word in words:
                print(f"{word}\t1")
    except Exception:
        continue

