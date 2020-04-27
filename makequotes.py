import json
from os import listdir
from os.path import isfile, join

# Get all of the files within a given directory
onlyfiles = [f for f in listdir("projectdata/jan-epoch2") if isfile(join("projectdata/jan-epoch2", f))]
list_of_files = []

# Add only core dataset files within the directory to list_of_files
for i in onlyfiles:
	if i[-5:] == ".json":
		if i[:2] != "._":
			print(i)
			list_of_files.append(i)

uniqueids_list = []

# Open all epochs within a timeframe (i.e. summer, jan, or march), open their uniqudids.txt files, and add to uniqueids_list
with open('projectdata/jan-epoch1/uniqueids.txt', 'r') as uniqueids, open('projectdata/jan-epoch2/uniqueids.txt', 'r') as uniqueids2:
	for i in uniqueids:
		uniqueids_list.append(int(i))
	for i in uniqueids2:
		uniqueids_list.append(int(i))

# For each file in the epoch
for i in list_of_files:
	quote_file = i[:-5] + "-quotes.json"
	print(i + " -> " + quote_file)

	# For each of these files, we will read from them, and then write out the tweets being referenced in quoted tweets, that AREN'T within the dataset themselves
	with open(("projectdata/reduced-jan-epoch2/" + quote_file), 'w+') as quotefile, open(("projectdata/jan-epoch2/" + i), 'r') as json_file:
		count = 0
		
		# For each tweet in the given file
		for tw in json_file:
			tweet = json.loads(tw)

			# We're looking specifically for the tweets that people are calling out as 'Fake', so we're looking only for quote tweets here
			# We must ensure the tweet is not a retweet OF a quote tweet, so we check for this
			if "retweeted_status" not in tweet and "quoted_status" in tweet:

				# If the tweet being referenced in the quote tweet isn't within our dataset (meaning it doesn't contain the words 'fake', or 'propoganda' etc.)
				if tweet["quoted_status"]["id"] not in uniqueids_list:

					# Add this tweet being referenced to the reduced-epoch folder
					count += 1
					if count % 1000 == 0:
						print(str(count) + " lines added to " + quote_file)
			
					data = {}

					data['tweet_id'] = int(tweet['quoted_status']['id'])
					data['username'] = tweet['quoted_status']['user']['screen_name']
		
					# If the tweet text has been shortened, we need to look at it's 'extended_tweet''s information
					if "extended_tweet" in tweet["quoted_status"]:
						data['text'] = tweet['quoted_status']['extended_tweet']['full_text']
						data['urls'] = tweet["quoted_status"]["extended_tweet"]["entities"]["urls"]
						data['quoted_users'] = tweet["quoted_status"]["extended_tweet"]["entities"]["user_mentions"]
						data['hashtags'] = tweet["quoted_status"]["extended_tweet"]["entities"]["hashtags"]
					else:
						data['text'] = tweet["quoted_status"]["text"]
						data['urls'] = tweet["quoted_status"]["entities"]["urls"]
						data['quoted_users'] = tweet["quoted_status"]["entities"]["user_mentions"]
						data['hashtags'] = tweet["quoted_status"]["entities"]["hashtags"]

					data['favorite_count'] = tweet['quoted_status']['favorite_count']
					data['quote_count'] = tweet['quoted_status']['quote_count']
					data['retweet_count'] = tweet['quoted_status']['retweet_count']
					json.dump(data, quotefile)
					quotefile.write("\n")

	print("\n")

				