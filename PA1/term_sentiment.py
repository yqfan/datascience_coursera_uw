import sys
import json
import re

def hw():
    print 'Hello, world!'

def lines(fp):
    print str(len(fp.readlines()))

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    sent_fname = sys.argv[1]
    tweet_fname = sys.argv[2]

    # set up the scores dict
    scores = {}
    with open(sent_fname) as sf:
        for line in sf:     
            term, score = line.split("\t")
            scores[term] = int(score)

    # calculate score for every word in all the tweets
    # terms is a larger dict like scores
    terms = {}
    with open(tweet_fname) as tf:
        for line in tf:
            tweet = json.loads(line)
            if 'text' in tweet:
                tweetText = tweet['text']
                # sc will be the score of this tweet according to dict 'scores'
                sc = 0
                for k,v in scores.items():
                    if k in tweetText:
                        sc += v
                
                # split the tweet into words, by space or punctions
                words = re.compile("[\s\.\?,!]").split(tweetText)

                # score of w = sum of scores of all the tweets that contain w.
                for w in words:
                    if w not in scores:
                        if w in terms:
                            terms[w] += sc
                        else:
                            terms[w] = sc
    for k, v in terms.items():
        print k + ' ' + str(v)
    sf.close()
    tf.close()        
if __name__ == '__main__':
    main()
