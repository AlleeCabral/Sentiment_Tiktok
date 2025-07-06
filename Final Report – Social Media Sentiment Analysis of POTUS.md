# Final Report – Social Media Sentiment Analysis of POTUS

**Student Name:** Alexandre Cabral and Jordan Schmutzler
 **Course:** PS25 - SE 02 Big Data & Analytics
 **Date:** 2025-07-04

-------

## 1. Introduction

This project is a sentiment analysis of the brand "Trump" in the context of a specific international crisis: a U.S. military attack on Iran ordered by President Trump. The study focuses on public reaction as expressed in a single Reddit thread from the subreddit r/AskReddit titled *"Trump bombs Iran. What do you think this will lead to?"* ([link](https://www.reddit.com/r/AskReddit/comments/1lhajc3/trump_bombs_iran_what_do_you_think_this_will_lead/)). It’s about understanding brand dynamics under pressure.

The analysis involved building a full data pipeline: collecting comments with Python, cleaning and processing them via Hadoop MapReduce, storing results in PostgreSQL, and performing sentiment classification in Python. Results give us insight into the polarity and emotional weight behind the reactions.

------

## 2. Problem Definition & Data Collection

### 2.1 Problem Statement

To analyze how a U.S. military strike on Iran ordered by President Trump affected public perception of his persona as a brand, by performing sentiment analysis on user comments from a specific Reddit thread in r/AskReddit.

### 2.2 Data Acquisition

#### 2.2.1 Reddit App creation - secret key

![](/home/alex/UE-Germany/Pictures/reddit_dev_landing.png)

#### 2.2.2 Reddit API

- **Search Term:**`Trump`

- **Posts Collected:** Approx. 7000 posts/comments retrieved using search queries on Reddit

- **Tool Used:** Python Reddit API Wrapper (PRAW) and direct JSON data storage.

![](/home/alex/UE-Germany/Pictures/potus_reddit_1.png), ![](/home/alex/UE-Germany/Pictures/potus_reddit_2.png)

- Data collected and stored in structured JSON format
- File stored locally as `reddit_trump_comments.json`



------

## 3. Data Engineering Environment Setup

### 3.1 Technical Configuration

- **OS:** Ubuntu 22.04
- **Java Version:** OpenJDK 11 (JAVA 11) selected and set correctly using `JAVA_HOME` and `update-alternatives`.
- **Hadoop Version:** 3.3.6
- **Python Environment:** Virtualenv with `nltk`, `TextBlob`, `VADER`, `psycopg2`, and other required libraries
- **Shell:** zsh configured via `.zshrc`

- **Java Version:** 
- **Hadoop Version:** 3.3.6 installed and configured.
- **Hadoop Services Running:** `NameNode`, `DataNode`, `ResourceManager`, `NodeManager`, `SecondaryNameNode`.

### 3.2 Challenges Resolved

- Incompatible Java version (Java 24) was replaced with Java 17 to support Hadoop, then again replaced by Java 11 for compatibility reasons.
- Manually launched YARN components when automatic launch failed.



------

## 4. Data Preprocessing with MapReduce

### 4.1 Cleaning Goals

- Remove stopwords, URLs, punctuation, emojis
- Normalize to lowercase
- Remove duplicates and missing values

### 4.2 mapperflatter.py (Python)

![](/home/alex/UE-Germany/Pictures/mapper.png)

This script is called "mapperflatter" because it not only maps over each object in the input array (processing each record individually), but also "flattens" the structure by emitting each word from the 'body' field as a separate output line. This flattening transforms nested or grouped data into a simple, line-by-line format suitable for further processing in data pipelines.

### 4.3 reducer.py (Python)

![](/home/alex/UE-Germany/Pictures/reducer.png)

### 4.4 Execution Command

```bash
~/UE-Germany/ps25_bigdata/Sentiment_Tiktok/scripts on  Setup! ⌚ 14:24:59
$ hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
  -D mapreduce.framework.name=local \
  -D fs.defaultFS=file:/// \
  -files /home/alex/UE-Germany/ps25_bigdata/Sentiment_Tiktok/scripts/mapperflatter.py,/home/alex/UE-Germany/ps25_bigdata/Sentiment_Tiktok/scripts/reducer.py \
  -input /home/alex/UE-Germany/ps25_bigdata/Sentiment_Tiktok/scripts/data/raw/reddit_trump_comments.json \
  -output /home/alex/UE-Germany/ps25_bigdata/Sentiment_Tiktok/scripts/output_local \
  -mapper mapperflatter.py \
  -reducer reducer.py \
  -cmdenv PYTHONIOENCODING=utf8 \
  -cmdenv PATH=/home/alex/UE-Germany/ps25_bigdata/Sentiment_Tiktok/.venv/bin:/usr/bin:/bin

```



------

## 5. Data Integration with PostgreSQL

### 5.1 Transfer

- Cleaned output from Hadoop loaded into PostgreSQL

![](/home/alex/UE-Germany/Pictures/postgresql_terminal.png)

### 5.2 FINALLY, first output... (underwhelming)

![](/home/alex/UE-Germany/Pictures/output_sample.png)

## 6. EDA (Notebook-Based)

The main exploration was performed in Jupyter Notebook

### 6.1 Tools Used

<img src="/home/alex/UE-Germany/Pictures/imports.png" style="zoom:67%;" />

### 6.2 Simple Visualizations for exploratory data analysys

- **Main dataframe** (comments_df)

  ![](/home/alex/UE-Germany/Pictures/comments_df.png)
  

- **Most active users, count of comments over time, avrg chars per comment**

<img src="/home/alex/UE-Germany/Pictures/active_users.png" style="zoom:67%;" />, <img src="/home/alex/UE-Germany/Pictures/comments_time.png" style="zoom:67%;" />, 

<img src="/home/alex/UE-Germany/Pictures/avrg_char.png" style="zoom:67%;" />



### 6.2 Sentiment Classification Logic

- Polarize text (scores from -1 to +1)
- Score each comment with compound sentiment value

### 6.3 Findings 

![image-20250704212059738](/home/alex/.config/Typora/typora-user-images/image-20250704212059738.png)

![image-20250704212259234](/home/alex/.config/Typora/typora-user-images/image-20250704212259234.png)![image-20250704212354559](/home/alex/.config/Typora/typora-user-images/image-20250704212354559.png)

![image-20250704212417225](/home/alex/.config/Typora/typora-user-images/image-20250704212417225.png)![image-20250704212504448](/home/alex/.config/Typora/typora-user-images/image-20250704212504448.png)

![image-20250704213132109](/home/alex/.config/Typora/typora-user-images/image-20250704213132109.png)

![image-20250704213148218](/home/alex/.config/Typora/typora-user-images/image-20250704213148218.png)





------

## 8. Conclusion & Recommendations

At first glance, the sentiment distribution in the thread appeared balanced—many users voiced either support or disapproval of Trump’s decision to bomb Iran. However, introducing the “score” parameter (upvotes) showed a more revealing picture: negative comments toward Trump consistently received the most support from the Reddit community. This suggests that, although users may have expressed a range of opinions, the platform sentiment leaned clearly against Trump’s action. This is a refreshing insight—showing that analyzing approval signals like upvotes can expose the dominant stance of a community.

Still, the analysis faced noise. The word cloud, for instance, is overly “cloudy,” cluttered with filler terms—pronouns, generic verbs, and function words—distracting from actual sentiment-bearing keywords. The word count metric suffers similarly, with “Iran” and "war" being the only standout terms. This points to the need for a stronger data cleaning and preprocessing pipeline in future work—more aggressive stopword filtering, *lemmatization* (*reduction to dictionary form. Ex.: running > run* ), and perhaps custom dictionaries.

A compelling next step would be to extract tuples combining sentiment-driven words with strong action verbs (e.g., “will,” “can’t,” “hate,” “trust”) to uncover more contextually rich sentiment expressions. This could help reclassify some “neutral” comments that actually carry strong emotional cues. More broadly, combining score-weighted sentiment, advanced phrase extraction, and a topic modeling layer could lead to a sharper and more actionable understanding of how public opinion shapes around a political brand in times of crisis.

------

