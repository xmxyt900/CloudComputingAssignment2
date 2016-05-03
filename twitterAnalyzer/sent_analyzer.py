import re
import json
import string

from nltk.corpus import stopwords
from collections import Counter

from sent_analyzer import sent_analyse

FLUE_KEYWORDS = ['flu', "influenza", "sore throat", "headache", "political"]  # must filter just english ones
AUSTRALIAN_ELECTION = ["auspol", "ausvotes", "elections2016", "election2016", "ausvotes2016"]
ELECTION_KEYWORDS = [['liberalparty', 'liberal', 'liberals', 'voteliberal', 'liberalaus', 'ausliberal'],
                     ['laborparty', 'labor', 'laboraus', 'auslabor', "alp"], ['thenationals', "npa"], ['lnp'],
                     ["greeens"]]
DRINKING_BEHAVIOUR = ["drunk", "wasted", "buzzed", "trashed", "blacked out", "hammered",
                      "intoxicated", "inebriated", "under the influence", "plastered", "juiced", "sauced"]

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>',  # HTML tags
    r'(?:@[\w_]+)',  # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',  # URLs

    r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
    r'(?:[\w_]+)',  # other words
    r'(?:\S)'  # anything else
]

tokens_re = re.compile(r'(' + '|'.join(regex_str) + ')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^' + emoticons_str + '$', re.VERBOSE | re.IGNORECASE)

punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via']


# start replaceTwoOrMore
def replaceTwoOrMore(s):
    # look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)


def process_tweet(tweet):
    # Convert to lower case
    tweet = tweet.lower()
    # Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet)
    # Convert @username to AT_USER
    tweet = re.sub('@[^\s]+', 'AT_USER', tweet)
    # Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    # Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    # trim
    tweet = tweet.strip('\'"')
    return tweet


def keyword_analysis(tweet):
    for k in FLUE_KEYWORDS:
        matches = re.compile(r'\b({0})\b'.format(k), flags=re.IGNORECASE).search(tweet)
        if matches:
            result = matches.groups()
            return {"flu": len(result)}
        return False


def data_summary(iterator_obj):
    out = open("place.txt", "w")
    # line = f.readline() # read only the first tweet/line
    keys = {u'place', u'geo', u'coordinates', u'location', u'actor', u'lang'}
    i = 0
    cnt = Counter()
    for line in iterator_obj:
        process_tweet(line)
        try:
            tweet = json.loads(line)  # load it as Python dict
            i += 1
        except ValueError:
            continue

        for k in keys:
            if tweet.get(k):
                cnt[k] += 1
        if tweet.get(u'place'):
            print()

    out.close()


def tokenize(s):
    return tokens_re.findall(s)


def get_tokens(s, lowercase=True):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
        # remove stop words
    tokens = [term for term in tokens if term not in stop]
    return tokens


def get_hash_tags(tokens):
    return [term for term in tokens if term.startswith('#')]


def summary(tweet_dict):
    t_list = get_tokens(tweet_dict['text'])
    h_list = get_hash_tags(t_list)
    data = {}
    result = {}
    for k in AUSTRALIAN_ELECTION:
        if "#{0}".format(k) in h_list:
            data.update({"auspol": True})
            break

    for party_list in ELECTION_KEYWORDS:
        for k in party_list:
            if k in t_list or "#{0}".format(k) in h_list:
                data.update({party_list[0]: True})
                break

    for k in DRINKING_BEHAVIOUR:
        if k in t_list:
            data.update({"drink": True})
            break

    if ("negativegearing" in t_list or "#negativegearing" in h_list or ("negative gearing" in tweet_dict['text'])):
        data.update({"negativegearing": True})
    if data:
        result['analysis'] = data
    result['sentiment'] = sent_analyse(tweet_dict['text'].replace("negative gearing", "negativegearing"))
    return result
import tweepy
import time
import re
import couchdb
import json
from tweepy.parsers import JSONParser
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import time
from analyzer import summary

VmIPs = list()
CouchDB = list()
Database = list()
backDatabase = list()

f = open('VmList', 'r')
for line in f:
    line = line.replace('\n', '')
    VmIPs.append(line)

for IPs in VmIPs:
    couchServer = couchdb.Server(IPs)
    CouchDB.append(couchServer)

totalCouchServer = len(CouchDB)

for index in range(totalCouchServer):
    try:
        db = CouchDB[index]['twitter_data']
        bdb = CouchDB[(index+1)%totalCouchServer]['backup_twitter_data']
    except:
        db = CouchDB[index].create('twitter_data')
        bdb = CouchDB[(index+1)%totalCouchServer].create('backup_twitter_data')
    Database.append(db)
    backDatabase.append(bdb) 

access_token = ["325310357-JbgtF1ZE5i3JYCTG0IKAp0LqYAhRNbz8ALCCxpZM","325310357-nGk5Uh3zp8kl0usaMcF2ctRpFqzK50vHEQMIsmRH","325310357-eSqI0Sy8Pfg0FGiGkHOEXdqQx2DD0upmTXjIbUkO","325310357-Hx0XYw9KCkyLaV7IHILv64NUTu1L8akArrj2GOgv","325310357-pZqvKzF7lSSRlON8zbgTpXkbCFnWe0jFAVP3YntJ","325310357-3dEXWkyTgHvODy587gLE9bHvLN27ZHY74qyJRkoJ","325310357-oS9cuOpUu9TusMRGMu5KodzQaAUbvHAWkSTk7Lz6","325310357-30FM4hrl0tqmVnJIk5KQiKgMu0e9xg1XgzoJdQln","719680431176724480-tJahXgUT0w889xws5sctek3y5ndNljh","719680431176724480-aDEB060aycA5hxTtLhocUGuNZlsBueB","719680431176724480-1KUVdXptX2fZkVHsKzyaZThsX66aV0E","719680431176724480-JOihW5kNj0YaTPkGzjhCiu4TF9tXK7W","719680431176724480-kSjw1RdJhDmZvcxQBU4KW1KEJfa9J2f","719680431176724480-Et2ykDj7O8uedLYj7r6MT79zBPTXDFm"]
access_token_secret = ["GNBnueRVTXazHG8N3zj5836IpxGe9ShQpor6S2bXtvP5G","zGQbHPSc2GOZOeCOBW1A3VEHloYGjZfVwxJfDftOHMmg1","WZEL8wjdGO2P0cTck7sm9m7pcXhOQM8sneJlxYAGwBa27","UFHOogA9HzZVpqmdxn8Lc28VnpPz7HRsVceRGqNGBXuRv","lfyV2yzA8rouZ8LB5aJUdIs9LpxSjc5wxPDdQjyPBI9AT","p76lE2p9RGIl6CTwkowZMlsTF0Ea4ma77MjSuKPaH264L","DwUnkVOjZ8J5xEtbBiRV4UJqtjsmgc9rrYOy6B3l09OaA","dJeONcprSzttwEUhae6xbdyxeSwUs2LXZHnJ4m0nN9ztn","EoHAoPuRaSUl67sdNi7pWCsOkK2afjkAYBGzcosN6ISs6","2e53UuxuEW9FXtO5R8kdQwNjGn0G3u8TiEHCopeRAy3cE","I6R2OUSfRN7NaIRWNFZdVoM4zlZecYvnzygvLiNWNeEmr","1qIkxisE6Yw5FYiq7Cx83kDtzBw4fUnvgI22PIYetNWkm","rhNFa53hTNTGk0x6l5Za2Lhas4m1yX2eh0SXcfzQIvfbd","zl5SoumEXYI5i9JRzhOzmWJta6Dmtmty5YcocrrgQP3UW"]
consumer_key = ["R1jKVExrbj7s3ysdnXdZKeagb","Bdid9UfnX8m3WNnaLRaGzAmrv","JpQeociWyi5887mAXW3KXiybS","1bppqTLMPLKejt3N6eeWFkM3M","i2piOL0m4u3VBVU2f5syhATyh","S3YTObqdIZGonFfpBs1rwqkqx","2l3AW9bC7lR3AqIrByKgNickm","KUHJuj4TYDBkuOO6Gi3GM9u1x","7SrBr2TMOwrIfrH0jX9GbQHEi","eYeyXEJ3Yepr2BTrzFbLuiaL8","9PTsp7byZbfq7b4SV4YzRUPcb","ZrmM4A8Lw7a8v7N3CbmMfN078","k66lgbELyjNnKNzYQCKdshiaR","oC7z1mebj6LOphEGHh4Gqlnlz"]
consumer_secret = ["tNF1tT289O9PyMY6hV0nIt1W8yHoyYjtYAo6Cc4gVHNpw2plNH","YhLZU3Gj2NpJ22jELmV4OnYSgNKao1dRIeYKwJUIAF9taJQn4E","QLJuaCZsPlCReisNn7dafgVlJvIcCnpaddbvwegwusMeE7mNo0","UpaJYyYZA1BY4t7ocVns60pPNMc7VI1Dv9VvNlnzLnxPaLZ8mg","9cNnnXKUiVOwbbXDBOKNTz3PUIa1dS7c4QdxjQ2hFW0KWAw9Po","jFG3UOkcgOnl0XpLMxgECyHwMVa9R6ngDcxEhkjAqLXvqtBsBa","aDDrbOB7Uzj00gBN96ha8nnTDc7qJsgvR84Z4GBF1PCIQMHew7","Md0WAYck8hZHBd0x83r6xmcTb4A4qHiSadQsYxKNp3MCWtqlD0","BZBxKuDHb1eBjrvhwQIYnsDxFfsaV80qrN7JFxA4ulNqiJUPec","2zVzCMnMZz66llXx47lPJ5c2YhxC7XI23ZIGEQyKFjO0BbUi01","a8zSYadBTSfGmKJwQUyBUzuf5c1oUxzggXZA5xAYgJGRKfhj2Y","pdAhuRmxONFpGBMfHiaRz99cQD0ET0ya3ILwvdoS57wVrjtSaF","c2yimuDZCrwwnvlqp2zJrv5HeOKXPlszvfyBvyHZfjHCeQoG5J","YhWVeqzkJF4TW5wBRyPTG7AoYAU3CqW0Zhn2kAmjAsLLeRb6G6"]

class StdOutListener(StreamListener):

    def on_data(self, data):
        if len(data)>1:
	    try:	
	        doc = json.loads(data)
		doc['_id'] = str(doc['id'])
		doc['result'] = summary(doc)
		dbID = abs(hash(doc['_id']))%totalCouchServer
		Database[dbID].save(doc)
		backDatabase[dbID].save(doc)
	    except (ValueError,couchdb.http.ResourceConflict) as e:
                pass
        return True

    def on_error(self, status_code):
        time.sleep(60*15)
        return True

if __name__ == '__main__':

    stream_listener = StdOutListener()
    auth = OAuthHandler(consumer_key[0], consumer_secret[0])
    auth.set_access_token(access_token[0], access_token_secret[0])
    stream = Stream(auth, stream_listener)
    stream.filter(locations=[144.3944921,-38.2607199,145.76474,-37.4598457])
        
