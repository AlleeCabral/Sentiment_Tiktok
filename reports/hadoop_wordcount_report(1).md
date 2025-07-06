# Hadoop Word Count with Streaming - Report

## 1. Environment Setup

- **OS:** Ubuntu 22.04
- **Java Version:** OpenJDK 17
- **Hadoop Version:** 3.x
- **Python Environment:** Virtualenv with NLTK installed

## 2. Input Data

- **File:** `reddit_trump_comments.json`
- **Format:** JSON objects, one per line, with the field `"body"` containing comment text.

## 3. Mapper Script (mapper.py)

```python
#!/usr/bin/env python3
import nltk
nltk.download('stopwords')
import sys, json, re
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
```

## 4. Reducer Script (reducer.py)

```python
#!/usr/bin/env python3
import sys

current_word = None
current_count = 0

for line in sys.stdin:
    word, count = line.strip().split('\t')
    count = int(count)
    if word == current_word:
        current_count += count
    else:
        if current_word:
            print(f"{current_word}\t{current_count}")
        current_word = word
        current_count = count

if current_word:
    print(f"{current_word}\t{current_count}")
```

## 5. Hadoop Streaming Local Command

```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -D mapreduce.framework.name=local \
  -D fs.defaultFS=file:/// \
  -input /home/alex/UE-Germany/ps25_bigdata/Sentiment_Tiktok/scripts/data/raw/reddit_trump_comments.json \
  -output /home/alex/UE-Germany/ps25_bigdata/Sentiment_Tiktok/scripts/output_local \
  -mapper mapper.py \
  -reducer reducer.py \
  -file /home/alex/UE-Germany/ps25_bigdata/Sentiment_Tiktok/scripts/mapper.py \
  -file /home/alex/UE-Germany/ps25_bigdata/Sentiment_Tiktok/scripts/reducer.py \
  -cmdenv PYTHONIOENCODING=utf8 \
  -cmdenv PATH=/home/alex/UE-Germany/ps25_bigdata/Sentiment_Tiktok/.venv/bin:/usr/bin:/bin
```

## 6. Sample Output

```
trump	4321
election	980
vote	850
america	790
...
```

## 7. Notes

- Job successfully run in local mode.
- Data was read and cleaned from JSON format.
- Output provides word frequency after removing stopwords.

## Next Steps

Proceed to:

- Export results to PostgreSQL
- Perform SQL-based analysis
- Conduct sentiment classification with Python
- Visualize the results in Tableau or Python

