import json
from collections import Counter
from os import listdir
from os.path import isfile, join

# Get all of the files within a given directory
onlyfiles = [f for f in listdir("projectdata/reduced-jan-epoch2") if isfile(join("projectdata/reduced-jan-epoch2", f))]

list_of_files = []

# Add only core dataset files within the directory to list_of_files
for i in onlyfiles:
	if i[:2] != "._" and i[:3] != "mos":
		list_of_files.append(i)

id_list = {}

number_of_tweets = 0
number_of_ids = 0

# For each file in the epoch
for i in list_of_files:
	print(i)
	# Open each of these files (containing only the referenced tweets from the original dataset)
	with open(("projectdata/reduced-jan-epoch2/" + i), "r") as json_file:
		# Add the ID of the tweet to id_list dictionary (we're creating a dictionary of the number of times each tweet has been referenced)
		for tw in json_file:
			number_of_tweets += 1
			tweet = json.loads(tw)
			id = tweet['tweet_id']
			if id not in id_list.keys():
				id_list[id] = 1
				number_of_ids += 1
			else:
				id_list[id] += 1

frequent_dict = []

# For each ID within the id_list dictionary
for i in id_list.keys():
	# Add the ID and the tweet information to frequent_dict list objects
	if id_list[i] > 0:
		frequent_dict.append((i, id_list[i]))

list_of_frequent = []
print(frequent_dict)
freq_dict = {}

# Add the number of times the tweet has been referenced to freq_dict dictionary
for i in frequent_dict:
	list_of_frequent.append(i[0])
	freq_dict[i[0]] = i[1] - 1

# Open the JSON file where this information will be stored
with open("projectdata/reduced-jan-epoch2/mostprovocative.json", "w+") as outfile:
	# For each file in the epoch
	for i in list_of_files:
		# Open the file 
		with open(("projectdata/reduced-jan-epoch2/" + i), "r") as json_file:
			for tw in json_file:
				tweet = json.loads(tw)
				# If the ID of the tweet is in our list of frequently called out tweets
				if tweet['tweet_id'] in list_of_frequent:
					
					# Add the tweet information to the outfile, alongside the number of times that tweet was called out in this epoch
					tweet['count'] = freq_dict.get(tweet['tweet_id'])
					quoted_users = []
					for i in tweet['quoted_users']:
						try:
							quoted_users.append(i['screen_name'])
						except TypeError:
							quoted_users.append(i)
					tweet['quoted_users'] = quoted_users
					urls_list = []
					for i in tweet['urls']:
						try:
							urls_list.append(i['expanded_url']) 
						except TypeError:
							urls_list.append(i)
					tweet['urls'] = urls_list
			
					json.dump(tweet, outfile)
					outfile.write("\n")
					
outfile.close()

print(str(number_of_tweets))
