# Sentiment Analysis on Tweets

As part of Data Mining, Text Mining and Big Data Analytics exam, I performed a sentiment analysis on a  supervised dataset of tweets [Twitter Hate Speech](https://www.kaggle.com/arkhoshghalb/twitter-sentiment-analysis-hatred-speech).

The objective of this task is to detect hate speechin tweets.For the sake of simplicity, we say a tweet contains hate speech if it has a racist or sexist sentiment associated with it. So, the task is to classify racist or sexist tweets from other tweets.Formally, given a training sample of tweets and labels, where label '1' denotes the tweet is racist/sexist and label '0' denotes the tweet is not racist/sexist, your objective is to predict the labels on the test dataset.This project is focused on comparing different text representations and learning models on a classification task.

The below 3 text representation strategies are:
* Bag-of-Words (BoW)
* TF-IDF
* Word2Vec (w2v)
* Doc2vec (d2v)

and comparing 3 classifiers:
* Logistic Regression
* Suport Vector Machine
* XGBoost


## Project WorkFlow
--------------------------------------------
* Import Libraries
* Tweets Preprocessing and Cleaning
    * Data Inspection
    * Data Cleaning
* Visualization from Tweets
* Extracting Features from Cleaned Tweets
    * Bag-of-Words
    * TF-IDF
    * Word2Vec
    * Doc2vec
* Model Building: Sentiment Analysis
    * Logistic Regression
    * Support Vector Machine
    * XGBoost
* Model Fine-tuning
* Summary

(Please refer to the [NoteBook](https://colab.research.google.com/drive/1zLdwPLBOTdNhVMXyFJ1oWxcAC-hytHjq#scrollTo=7uBIlZbCb3JW) for a more detailed description.)

## How to Run
----------
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1GD3Nsl_l9LXJhg2FmzUsqNWQACoD6-Ti?usp=sharing)


## Models Training
---------------------------------
I fine tuned XGBoost + Word2Vec with  tree-specific parameters such as max_depth, min_child_weight, subsample, colsample_bytree keeping the learning rate fixed.Tune the learning rate and Finally tune gamma to avoid overfitting.


## Results
--------------------------------------
Here are the models F1-score on Validation set.
![resultslatest](https://user-images.githubusercontent.com/72126242/150693346-324ca094-37db-440e-a053-352ffdefc89b.png)

## Built With
---------------------------------
Python 3.7

## Author
-------------------------------
[Jyoti Yadav](https://www.linkedin.com/in/jyoti-yadav-64916b160/)


