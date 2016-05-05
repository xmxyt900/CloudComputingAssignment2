import json
import pandas
import vincent
import couchdb
import json
import os


from collections import Counter
from vincent import AxisProperties, PropertySet, ValueRef

from analyzer import get_tokens
from sent_analyzer import sent_analyse


def generate_geo_data(tweet_dict):
    geo_json_feature = {}
    if tweet_dict['coordinates']:
        geo_json_feature = {
            "type": "Feature",
            "geometry": tweet_dict['coordinates'],
            "properties": {
                "text": tweet_dict['text'],
                "created_at": tweet_dict['created_at'],

            }
        }


    elif tweet_dict['place']:
        b_box = tweet_dict['place']['bounding_box']['coordinates']
        x_center = (b_box[0][1][0] + b_box[0][2][0]) / 2
        y_center = (b_box[0][2][1] + b_box[0][3][1]) / 2
        geo_json_feature = {
            "type": "Feature",
            "geometry": {'type': 'Point', 'coordinates': [x_center, y_center]},
            "properties": {
                "text": tweet_dict['text'],
                "created_at": tweet_dict['created_at']
            }
        }

    return geo_json_feature


def generate_data(tweet_dict):
    s_a = tweet_dict['sentiment']
    geo_features = generate_geo_data(tweet_dict)

    # location data for map
    if geo_features:
        geo_features['properties']['sent'] = s_a['pos'] - s_a["neg"]
        geo_data['features'].append(geo_features)

    token_list = get_tokens(tweet_dict['text'])
    # hash frequency
    terms_hash = [term for term in token_list if term.startswith('#')]
    count_hashs.update(terms_hash)

    # term frequency
    terms_token = [term for term in token_list]
    count_terms.update(terms_token)

    # for time chart
    timestamps.append(tweet_dict['created_at'])
    pos_ar.append(s_a["pos"])
    neg_ar.append(s_a["neg"])
    neu_ar.append(s_a["neu"])


def generate_files(arg):

    term_file_name = "term_freq_" + arg + ".json"
    hash_file_name = "hash_freq_" + arg + ".json"
    chart_file_name = "time_chart_" + arg + ".json"
    sent_chart_file_name = "sent_time_chart_" + arg + ".json"
    geo_file_name = "geo_data_" + arg + ".json"
    geo_file_name_nsent = "geo_data_" + arg + ".json"
    geo_file_name_psent = "geo_data_" + arg + ".json"


    # file for map
    with open(geo_file_name, 'w') as fout:
        fout.write(json.dumps(geo_data, indent=4))

    def set_properties(bar, x_label='', y_label="Freq", padding=20):
        bar.height = 300
        bar.width = 600
        bar.axis_titles(x=x_label, y=y_label)

        ax = AxisProperties(labels=PropertySet(angle=ValueRef(value=70),
                                               dx=ValueRef(value=padding),
                                               font_size=ValueRef(value=11),
                                               font=ValueRef(value="Tahoma, Helvetica")
                                               ), title=PropertySet(dy=ValueRef(value=40)))
        bar.axes[0].properties = ax
        bar.scales['x'].padding = 0.2

    # file for hash frequency
    if count_hashs:
        word_freq = count_hashs.most_common(20)
        labels, freq = zip(*word_freq)
        data = {'data': freq, 'x': labels}
        bar = vincent.Bar(data, iter_idx='x')
        set_properties(bar, padding=25 + len(max(labels, key=len)))
        bar.to_json(hash_file_name)

    # file for term frequency
    if count_terms:
        word_freq = count_terms.most_common(20)
        labels, freq = zip(*word_freq)
        data = {'data': freq, 'x': labels}
        bar = vincent.Bar(data, iter_idx='x', padding=20 + len(max(labels, key=len)))
        set_properties(bar)
        bar.to_json(term_file_name)

    # file for time chart
    ones = [1] * len(timestamps)
    # the index of the series
    idx = pandas.DatetimeIndex(timestamps)
    # the actual series (at series of 1s for the moment)
    ITAvWAL = pandas.Series(ones, index=idx)
    # Resampling / bucketing
    per_hour = ITAvWAL.resample('30min').sum().fillna(0)
    time_chart = vincent.Line(per_hour)
    set_properties(time_chart, x_label='Time')
    time_chart.to_json(chart_file_name)

    # file for sentiment analysis
    idx = pandas.DatetimeIndex(timestamps)
    # the actual series (at series of 1s for the moment)
    ITAvWALp = pandas.Series(pos_ar, index=idx)
    ITAvWALn = pandas.Series(neg_ar, index=idx)
    ITAvWALnu = pandas.Series(neu_ar, index=idx)
    # Resampling / bucketing
    p_h = ITAvWALp.resample('12H').mean().fillna(0)
    p_n = ITAvWALn.resample('12H').mean().fillna(0)
    p_nu = ITAvWALnu.resample('12H').mean().fillna(0)
    xx = pandas.concat({"positove": p_h, "negative": p_n, "neutral": p_nu}, axis=1)
    time_chart = vincent.Line(xx)
    set_properties(time_chart, x_label='Time')
    time_chart.legend(title="catgeories")
    time_chart.to_json(sent_chart_file_name)


viewArray = ['drink_true', 'negativegearing_true', 'political_true']
ext = ['dr', 'neg', 'pol']


couch = couchdb.Server()
for index in range(len(viewArray)):
    db = couch[viewArray[index]]
    count_terms = Counter()
    count_hashs = Counter()
    timestamps = []
    geo_data = {
        "type": "FeatureCollection",
	"features": []
    }
    geo_data_psent = {
	"type": "FeatureCollection",
        "features": []
    }
    geo_data_nsent = {
        "type": "FeatureCollection",
	"features": []
    }
    pos_ar = []
    neg_ar = []
    neu_ar = []
    for id in db:
        command = "curl -X GET http://127.0.0.1:5984/"+viewArray[index]+"/"+id
	res = os.popen(command).read()
	doc = json.loads(res)	
	generate_data(doc['value'])
    generate_files(ext[index])

