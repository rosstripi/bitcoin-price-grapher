"""
Bitcoin price aggregator
author: rossbot
"""

import twitter, re, sys, operator
import matplotlib.pyplot as pyplot
from dateutil.parser import parse

consumer_key        = #insert key
consumer_secret     = #insert key
# note: access tokens may have to be occasionally updated
access_token        = #insert key
access_token_secret = #insert key

api = twitter.Api(consumer_key, consumer_secret,
                  access_token, access_token_secret)

def fetch():
    data = {}
    max_id = None
    total = 0
    while True:
        statuses = api.GetUserTimeline(screen_name='bitcoinprice',
                                       count=200, max_id=max_id)
        newCount = ignCount = 0
        for s in statuses:
            if s.id in data:
                ignCount += 1
            else:
                data[s.id] = s
                newCount += 1
        total += newCount
        print >>sys.stderr, "Fetched %d/%d/%d new/old/total." % (
            newCount, ignCount, total)
        if newCount == 0:
            break
        max_id = min([s.id for s in statuses]) - 1
    return data.values()

def storeValues(tweets):
    for tweet in tweets:
        tweet.pdate = parse(tweet.created_at)
    key = operator.attrgetter('pdate')
    tweets = sorted(tweets, key=key)
    prices = {}
    exp = re.compile(r'[0-9]*\.[0-9][0-9]')
    for tweet in tweets:
        words = tweet.text.encode('utf8')
        if len(exp.findall(words))==1:
            prices[int(tweet.pdate.strftime('%Y%m%d%H%M'))] = float(exp.findall(words)[0])
    return prices
    
def plotPrices(prices):
    keys = sorted(prices.keys())
    dates = []
    values = []
    for key in keys:
        dates.append(key)
        values.append(prices[key])
    pyplot.plot(dates,values,'r-')
    pyplot.xlabel('date')
    pyplot.ylabel('value in USD')
    pyplot.show()
    


#execution of the program
if __name__ == '__main__':
    data = fetch()
    prices = storeValues(data)
    plotPrices(prices)
