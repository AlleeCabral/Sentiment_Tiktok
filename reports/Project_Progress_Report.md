# Sentiment Analysis Project Report (Progress Summary)

**Student Name:** Alex  
**Project:** Sentiment Analysis using Big Data Tools  
**Course:** PS25 - SE 02 Big Data & Analytics  
**Date:** 2025-07-04  

---

## 1. Project Setup

### 1.1 Environment Configuration
- **Shell:** `zsh` configured via `.zshrc`.
- **Java Version:** Java 17 selected and set correctly using `JAVA_HOME` and `update-alternatives`.
- **Hadoop Version:** 3.3.6 installed and configured.
- **Hadoop Services Running:** `NameNode`, `DataNode`, `ResourceManager`, `NodeManager`, `SecondaryNameNode`.

### 1.2 Challenges Resolved
- Incompatible Java version (Java 24) was replaced with Java 17 to support Hadoop.
- Resolved `clusterID` mismatch by reformatting HDFS storage.
- Manually launched YARN components when automatic launch failed.

---

## 2. Data Collection

### 2.1 Platform: Reddit
- **Search Term:** `Trump`
- **Posts Collected:** Targeting high-comment threads.
- **Tool Used:** Python Reddit API Wrapper (PRAW) and direct JSON data storage.

### 2.2 File Location
- Local: `~/reddit_trump_comments.json`
- HDFS: `/user/alex/reddit_data/reddit_trump_comments.json`

---

## 3. Hadoop Integration

### 3.1 Data Storage in HDFS
- Uploaded Reddit JSON data file using:  
  ```bash
  hdfs dfs -put -f ~/reddit_trump_comments.json /user/alex/reddit_data/
  ```
- Verified storage with `hdfs dfs -ls`.

---

## 4. Next Planned Steps (As per Assignment)

### 4.1 Data Cleaning (MapReduce)
- Remove stopwords, URLs, emojis.
- Handle missing values and duplicates.
- Normalize text for sentiment analysis.

### 4.2 Data Analysis
- Transfer cleaned data to PostgreSQL (or DBeaver-compatible DB).
- Perform SQL-based sentiment and trend analysis.
- Use Python libraries (TextBlob, VADER, NLTK) for sentiment classification.

---

## Notes
- DBeaver can be used as a PostgreSQL client interface.
- Continue documenting the process for final reporting and presentation.

