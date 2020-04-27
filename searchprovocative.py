import json
from collections import Counter

usernames = {}
calloutratio_list = {}
most_recent_list = {}

# Open up this epochs' most provocative tweets from mostprovocative.json
with open('projectdata/reduced-jan-epoch2/mostprovocative.json', 'r') as json_file:
	# For each of these tweets
	for tw in json_file:
		tweet = json.loads(tw)
		# Create a dictionary of each of these tweets, with their tweet_id being key, and their value being the tweet containing the highest quote_count
		# We do this as there will be multiple values of quote_count, retweet_count etc. between the same tweet from how this information has changed over time
		# And we want the most up-to-date version of this 
		if (tweet['tweet_id']) not in most_recent_list.keys():
			most_recent_list[(tweet['tweet_id'])] = tweet
		else:
			if tweet['quote_count'] > most_recent_list[(tweet['tweet_id'])]['quote_count']:
				most_recent_list[(tweet['tweet_id'])] = tweet

# Create a new json file to write these unique, up-to-date versions of each tweet to	
with open('projectdata/reduced-jan-epoch2/mostprovocativefinal.json', 'w') as outfile:
	for i in most_recent_list:
		tweet = most_recent_list[i]
		try:
			# Create a callout_ratio for each tweet, where we work out the ratio of tweets quoting them calling them out, vs. tweets just quoting them ordinarily
			tweet['callout_ratio'] = tweet['count'] / tweet['quote_count']
			json.dump(tweet, outfile)
			outfile.write("\n")
		except ZeroDivisionError:
			print(tweet['tweet_id'])
		
count = 0
outfile.close()

# Now we open the finalfocalcontent.json to write our final, most provocative and unique tweets from this epoch to
with open('projectdata/reduced-jan-epoch2/mostprovocativefinal.json', 'r') as input_file, open('projectdata/reduced-jan-epoch2/finalfocalcontent.json', 'w') as outfile:
	for tw in input_file:
		tweet = json.loads(tw)
		# We use callout_ratio to determine eligibility, in order to restrict anomalous callings out from affecting our results somewhat
		if tweet['callout_ratio'] > 0.01:
			if tweet['urls'] != []:
				json.dump(tweet, outfile)
				outfile.write("\n")
				for url in tweet['urls']:
					count += 1

print(str(count))

