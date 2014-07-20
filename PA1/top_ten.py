import sys
import json
import re
import heapq

def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    tweet_fname = sys.argv[1]

    # count_of is a dict with count of each hashtag in all tweets
    count_of = {}
    with open(tweet_fname) as f:
        for line in f:
            tweet = json.loads(line)
            
            # find the 'hashtag' dict in 'entities' field
            if 'entities' in tweet:
                entries = tweet['entities']
                if entries != None:
                    if 'hashtags' in entries:
                        hashtag_list = entries['hashtags']
                        for h in hashtag_list:
                            # text is a hashtag
                            # skip all non-English hashtag
                            text = h['text']
                            nonEnglish = re.compile("[^(0-9A-Za-z)]")
                            if nonEnglish.match(text) != None:
                                continue

                            # update count_of dict
                            if text in count_of:
                                count_of[text] += 1
                            else:
                                count_of[text] = 1

    # top_ten_heap contains top ten hashtags
    top_ten_heap = []

    # go through count_of dict for all hashtags
    # and update top_ten_heap
    for k, v in count_of.items():
        if len(top_ten_heap) < 10:
            heapq.heappush(top_ten_heap, (v, k))
            continue
        pair = top_ten_heap[0]
        if pair[0] < v:
            heapq.heappop(top_ten_heap)
            heapq.heappush(top_ten_heap, (v, k))

    # print top ten hashtags (the ten hashtags are not ordered)
    while len(top_ten_heap) > 0:
        pair = heapq.heappop(top_ten_heap)
        print pair[1] + ' ' + str(pair[0])
    f.close()

if __name__ == '__main__':
    main() 
