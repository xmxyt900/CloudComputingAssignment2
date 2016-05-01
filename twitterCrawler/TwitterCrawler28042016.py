import tweepy
import time
import re
import couchdb
import json
from tweepy.parsers import JSONParser

#there are 14 credentials from 0-13
access_token = ["325310357-JbgtF1ZE5i3JYCTG0IKAp0LqYAhRNbz8ALCCxpZM","325310357-nGk5Uh3zp8kl0usaMcF2ctRpFqzK50vHEQMIsmRH","325310357-eSqI0Sy8Pfg0FGiGkHOEXdqQx2DD0upmTXjIbUkO","325310357-Hx0XYw9KCkyLaV7IHILv64NUTu1L8akArrj2GOgv","325310357-pZqvKzF7lSSRlON8zbgTpXkbCFnWe0jFAVP3YntJ","719680431176724480-tJahXgUT0w889xws5sctek3y5ndNljh","719680431176724480-aDEB060aycA5hxTtLhocUGuNZlsBueB","719680431176724480-1KUVdXptX2fZkVHsKzyaZThsX66aV0E"]
access_token_secret = ["GNBnueRVTXazHG8N3zj5836IpxGe9ShQpor6S2bXtvP5G","zGQbHPSc2GOZOeCOBW1A3VEHloYGjZfVwxJfDftOHMmg1","WZEL8wjdGO2P0cTck7sm9m7pcXhOQM8sneJlxYAGwBa27","UFHOogA9HzZVpqmdxn8Lc28VnpPz7HRsVceRGqNGBXuRv","lfyV2yzA8rouZ8LB5aJUdIs9LpxSjc5wxPDdQjyPBI9AT","EoHAoPuRaSUl67sdNi7pWCsOkK2afjkAYBGzcosN6ISs6","2e53UuxuEW9FXtO5R8kdQwNjGn0G3u8TiEHCopeRAy3cE","I6R2OUSfRN7NaIRWNFZdVoM4zlZecYvnzygvLiNWNeEmr"]
consumer_key = ["R1jKVExrbj7s3ysdnXdZKeagb","Bdid9UfnX8m3WNnaLRaGzAmrv","JpQeociWyi5887mAXW3KXiybS","1bppqTLMPLKejt3N6eeWFkM3M","i2piOL0m4u3VBVU2f5syhATyh","7SrBr2TMOwrIfrH0jX9GbQHEi","eYeyXEJ3Yepr2BTrzFbLuiaL8","9PTsp7byZbfq7b4SV4YzRUPcb"]
consumer_secret = ["tNF1tT289O9PyMY6hV0nIt1W8yHoyYjtYAo6Cc4gVHNpw2plNH","YhLZU3Gj2NpJ22jELmV4OnYSgNKao1dRIeYKwJUIAF9taJQn4E","QLJuaCZsPlCReisNn7dafgVlJvIcCnpaddbvwegwusMeE7mNo0","UpaJYyYZA1BY4t7ocVns60pPNMc7VI1Dv9VvNlnzLnxPaLZ8mg","9cNnnXKUiVOwbbXDBOKNTz3PUIa1dS7c4QdxjQ2hFW0KWAw9Po","BZBxKuDHb1eBjrvhwQIYnsDxFfsaV80qrN7JFxA4ulNqiJUPec","2zVzCMnMZz66llXx47lPJ5c2YhxC7XI23ZIGEQyKFjO0BbUi01","a8zSYadBTSfGmKJwQUyBUzuf5c1oUxzggXZA5xAYgJGRKfhj2Y"]

#there are 16 locations from 0-15
location = ["-38.2607,144.3945,15km","-38.2607,144.73705,15km","-38.2607,145.0796,15km","-38.2607,145.4221,15km","-37.86025,144.3945,15km","-37.86025,144.73705,15km","-37.86025,145.0796,15km","-37.86025,145.4221,15km","-38.2607,144.73705,15km","-38.2607,145.0796,15km","-38.2607,145.4221,15km","-38.2607,145.7647,15km","-37.4598,144.73705,15km","-37.4598,145.0796,15km","-37.4598,145.4221,15km","-37.4598,145.7647,15km"]

#change the index i to number from 0-14
auth = tweepy.OAuthHandler(consumer_key[i],consumer_secret[i])
auth.set_access_token(access_token[i],access_token_secret[i])

api = tweepy.API(auth)

searched_tweets = []
last_id = -1
max_tweets = 1000000

while len(searched_tweets) < max_tweets:
    count = max_tweets - len(searched_tweets)
    try:
        #change the index i to number 0-15
		new_tweets = api.search(geocode=location[i],count=count, max_id=str(last_id - 1))
        if not new_tweets:
            break
        searched_tweets.extend(new_tweets)
        last_id = new_tweets[-1].id
        for tweet in new_tweets:
            json_data = json.dumps(tweet._json)
            print(json_data)
    except tweepy.TweepError:
        time.sleep(60*15)
        continue
    
