import sys
import json

def hw():
    print 'Hello, world!'

def lines(fp):
    print str(len(fp.readlines()))

def main():
    
    # transform unicode to utf-8
    reload(sys)
    sys.setdefaultencoding('utf-8')

    sent_fname = sys.argv[1]
    tweet_fname = sys.argv[2]

    #set up the scores dictionary
    scores = {}
    with open(sent_fname) as sf:
        for line in sf:
            term, score = line.split("\t")
            scores[term] = int(score)

    # for each tweet, look for its 'text' field
    # sum up the score of each word according to scores dict
    with open(tweet_fname) as tf:
        for line in tf:
            tweet = json.loads(line)
            if 'text' in tweet:
	        tweetText = tweet['text']
                # sc will be the score of this tweet
                sc = 0
                for k,v in scores.items():
                    if k in tweetText:
                        sc += v
                print sc
    sf.close()
    tf.close()   

if __name__ == '__main__':
    main()
