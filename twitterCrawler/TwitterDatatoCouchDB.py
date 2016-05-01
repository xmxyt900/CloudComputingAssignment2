#import regex
import re
FLUE_KEYWORDS=['flu', "influenza", "sore throat", "headache", "political"] #must filter just english ones
AUSTRALIAN_ELECTION=["auspol", "ausvotes", "elections2016", "election2016", "ausvotes2016"]
ELECTION_KEYWORDS=[['liberalparty', 'liberal', 'liberals','voteliberal', 'liberalaus', 'ausliberal'], ['laborparty', 'labor', 'laboraus', 'auslabor', "alp"], ['thenationals', "npa"], ['lnp'], ["greeens"]]
DRINKING_BEHAVIOUR = ["drunk", "wasted", "buzzed","trashed", "blacked out", "hammered",
                      "intoxicated", "inebriated", "under the influence", "plastered", "juiced", "sauced"]
#alcohol related tweets during night, weekends
EMOTICONS_STR = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
from nltk.corpus import stopwords
import string

punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via']


#start process_tweet
from collections import Counter
#start replaceTwoOrMore
def replaceTwoOrMore(s):
    #look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)
#end


def process_tweet(tweet):
    # process the tweets

    #Convert to lower case
    tweet = tweet.lower()
    #Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
    #Convert @username to AT_USER
    tweet = re.sub('@[^\s]+','AT_USER',tweet)
    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    #Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #trim
    tweet = tweet.strip('\'"')
    return tweet
#end


def keyword_analysis(tweet):
    for k in FLUE_KEYWORDS:
        matches = re.compile(r'\b({0})\b'.format(k), flags=re.IGNORECASE).search(tweet)
        if matches:
            result = matches.groups()
            return {"flu": len(result)}
        return False

import json

def data_summary(iterator_obj):
        out=open("place.txt", "w")
        #line = f.readline() # read only the first tweet/line
        keys={u'place',u'geo',u'coordinates', u'location', u'actor', u'lang'}
        i=0
        cnt = Counter()
        for line in iterator_obj:
            process_tweet(line)
            try:
                tweet = json.loads(line) # load it as Python dict
                i+=1
            except ValueError:
                continue

            for k in keys:
                if tweet.get(k):
                    cnt[k] += 1
            if tweet.get(u'place'):
                print()

        out.close()



emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs

    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

def tokenize(s):
    return tokens_re.findall(s)

def get_tokens(s, lowercase=True):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
        #remove stop words
    tokens = [term for term in tokens if term not in stop]
    return tokens

def get_hash_tags(tweet_dict):
    return [term for term in get_tokens(tweet_dict['text']) if term.startswith('#')]
def election_summary(tweet_dict):
    h_list=get_hash_tags(tweet_dict)
    election_data ={}
    for k in AUSTRALIAN_ELECTION:
        if "#{0}".format(k) in h_list:
            election_data.update({"auspol":True})
            break

    for party_list in ELECTION_KEYWORDS:
        for k in party_list:
            if "#{0}".format(k) in h_list:
                election_data.update({party_list[0]:True})
                break
            else:
                election_data.update({party_list[0]:False})



    return election_data

def drinking_summary(tweet_dict):
    h_list=get_tokens(tweet_dict['text'])
    drink_data ={}
    for k in DRINKING_BEHAVIOUR:
        if k in h_list:
            drink_data.update({"drink":True})
            break

    if ("negativegearing" in h_list or ("negative gearing" in tweet_dict['text'])):
        drink_data.update({"negativegearing":True})

    return drink_data



def start():

    with open('twitter.json') as f:
        for t in f:
            keyword_analysis(t)
