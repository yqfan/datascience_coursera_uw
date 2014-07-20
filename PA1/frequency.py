import sys
import json
import re

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    tweet_fname = sys.argv[1]

    # count is a dict recording show up time of each word in all tweets
    # total is total word count in all tweets
    count = {}
    total = 0

    with open(tweet_fname) as f:
        for line in f:
            tweet = json.loads(line)
            if 'text' in tweet:
                tweetText = tweet['text']
                words = re.compile("[\s\.\?,!]").split(tweetText)
                nonEnglish = re.compile("[^(0-9A-Za-z)]")
                for w in words:
                    if len(w) == 0:
                        continue
                    # skip non English words
                    if nonEnglish.match(w) != None:
                        continue
                    total += 1
                    if w in count:
                        count[w] += 1
                    else:
                        count[w] = 1
    for k, v in count.items():
        print ('%s %.4f'%(k, float(v)/float(total)))
    f.close()
if __name__ == '__main__':
    main()
