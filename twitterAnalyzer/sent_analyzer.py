from nltk.sentiment.vader import SentimentIntensityAnalyzer


def sent_analyse(text):
    # import math
    vader_analyzer = SentimentIntensityAnalyzer()
    sa = vader_analyzer.polarity_scores(text)

    # if sa['neu'] == 1:
    #  print('  - **{0}:**  \n'.format('neu'))
    sa['sent'] = False
    if sa['neu'] < sa['pos'] or sa['compound'] > 0.75:
        # print('  - **{0}:**  \n'.format(sa['pos']))
        sa['sent'] = True
    elif sa['neg'] > sa['pos'] or sa['compound'] < -0.75:
        # print('  - **{0}:**  \n'.format(sa['neg']))
        sa['sent'] = True

    return sa
