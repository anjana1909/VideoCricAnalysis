import csv
from itertools import islice
from threading import Thread
import nltk
from nltk.stem import *
sentiments=[]


    
def getSentimentData(x,y,pos,neg):
    with open('MDictionary.csv') as csvreader:
        senti = csv.reader(csvreader)
        for s in islice(senti,x,y):
            sentiment='neutral'
            if(int(s[neg])>0):
                sentiment='negative'
            if(int(s[pos])>0):
                sentiment='positive'
            if sentiment!='neutral':
                sentiments.append((s[0].lower().split(),sentiment))

pos=None
neg=None
with open('MDictionary.csv') as csvreader:
    senti = csv.reader(csvreader)
    num=len(list(senti))
with open('MDictionary.csv') as csvreader:
    senti = csv.reader(csvreader)
    for s in islice(senti,0,1):
        neg=s.index('Negative')
        pos=s.index('Positive')
        print(pos,neg)
    x=1
    y=400
    print(num,pos,neg)
    number_of_threads=(num-1)//400
    print(number_of_threads)
    threads=[]
    for i in range(0,number_of_threads):
        t=Thread(target=getSentimentData,args=(x,y,pos,neg))
        threads+=[t]
        t.start()
        x+=400
        y+=400
    t=Thread(target=getSentimentData,args=(x,num-1,pos,neg))
    threads+=[t]
    t.start()
    
    for x in threads:
        x.join()
        
#print(sentiments)


def get_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
      all_words.extend(words)
    return all_words

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features

def extract_features(document):
    document_words = set(document)

    features = {}
    for word in word_features:

        p=list(SnowballStemmer("english").stem(word) for word in document_words)
        p=set(p)

        features['contains(%s)' % word] = (word in p)
    return features

word_features = get_word_features(get_words_in_tweets(sentiments))

#print(word_features)
#print(len(word_features))

#extract_features('Virat bowled brilliantly'.split())
training_set = nltk.classify.apply_features(extract_features, sentiments)
#print(training_set)
classifier = nltk.NaiveBayesClassifier.train(training_set)
tweet = 'Virat bowled brilliantly'
print(classifier.classify(extract_features(tweet.split())))
