import sys
import json
import re
states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}
def main():

    reload(sys)
    sys.setdefaultencoding('utf-8')

    sent_fname = sys.argv[1]
    tweet_fname = sys.argv[2]
    scores = {}
    state_score = {}

    # abbr_of is the reverse dict of 'states'
    # get abbreviation given full state name
    abbr_of = {}
    for k,v in states.items():
        abbr_of[v] = k 

    # calculate the scores dict
    with open(sent_fname) as sf:
        for line in sf:
            term, score = line.split("\t")
            scores[term] = int(score)

    # calculate state_score dict, key is two-letter state abbreviation,
    # value is sum of scores of all tweets in this state
    with open(tweet_fname) as tf:
        for line in tf:
            tweet = json.loads(line)
            if 'text' not in tweet:
                continue
            if 'place' not in tweet:
                continue
            if tweet['place'] == 'null':
                continue
            tweetText = tweet['text']

            # find state in 'place' field
            placeDict = tweet['place']
            if placeDict == None:
                continue
            # skip tweets not in USA
            country = placeDict['country_code']
            if country != 'US':
                continue
            # state info is usually the last token in 'full_name' 
            tokens = placeDict['full_name'].split(",")
            tmp = tokens[-1].strip(' \t\r\n')
            # if the last token is 'USA', then get the last but one token
            if tmp == 'USA' and len(tokens) >= 2:
                tmp = tokens[-2].strip(' \t\r\n')
            state = ''
            # let state = two-letter abbreviation
            if tmp in abbr_of:
                state = abbr_of[tmp]
            elif tmp in states:
                state = tmp
            else:
                continue
            
            # sc is the score of this tweet
            sc = 0
            for k, v in scores.items():
                if k in tweetText:
                    sc += v

            # update state_score dict
            if state in state_score:
                state_score[state] += sc
            else:
                state_score[state] = sc

    # find the max score in state_score dict
    max_score = -9999 
    max_state = ''
    for k, v in state_score.items():
        if v > max_score:
            max_score = v
            max_state = k
    print max_state
    sf.close()
    tf.close()

if __name__ == '__main__':
    main()
