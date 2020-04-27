import json
import requests
import sys

summerepoch_list = {}
janepoch_list = {}
marchepoch_list = {}
similar_list = []

# Take arguments for the epochs we're comparing
time1 = sys.argv[1]
time2 = sys.argv[2]

# Sets variable for first set of epochs we're looking at
if time1 == "summer":
	list1_type = summerepoch_list
elif time1 == "jan":
	list1_type = janepoch_list
elif time1 == "march":
	list1_type = marchepoch_list

# Sets variable for second set of epochs we're looking at
if time2 == "summer":
	list2_type = summerepoch_list
elif time2 == "jan":
	list2_type = janepoch_list
elif time2 == "march":
	list2_type = marchepoch_list

# Function to find extended URL given a URL
def resolve_url(url):
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException:
        return (url, None)

    if r.status_code != 200:
        longurl = None
    else:
        longurl = r.url

    return (url, longurl)

# Opens all files, and adds their contents to their respective dictionaries
with open("projectdata/reduced-epoch1/finalfocalcontent.json", "r") as epoch1, open("projectdata/reduced-epoch2/finalfocalcontent.json", "r") as epoch2, open("projectdata/reduced-epoch3/finalfocalcontent.json", "r") as epoch3, open("projectdata/reduced-jan-epoch1/finalfocalcontent.json", "r") as janepoch1, open("projectdata/reduced-jan-epoch2/finalfocalcontent.json", "r") as janepoch2, open("projectdata/reduced-march-epoch1/finalfocalcontent.json", "r") as marchepoch1:
	for tw in epoch1:
		tweet = json.loads(tw)
		summerepoch_list[(tweet['tweet_id'])] = tweet
	for tw in epoch2:
		tweet = json.loads(tw)
		summerepoch_list[(tweet['tweet_id'])] = tweet
	for tw in epoch3:
		tweet = json.loads(tw)
		summerepoch_list[(tweet['tweet_id'])] = tweet
	for tw in janepoch1:
		tweet = json.loads(tw)
		janepoch_list[(tweet['tweet_id'])] = tweet
	for tw in janepoch2:
		tweet = json.loads(tw)
		janepoch_list[(tweet['tweet_id'])] = tweet
	for tw in marchepoch1:
		tweet = json.loads(tw)
		marchepoch_list[(tweet['tweet_id'])] = tweet

	count = 0

	# For each URL in each tweet in the first set of epochs
	for tw in list1_type.keys():
		for url in list1_type[tw]['urls']:
			# If the URL is within the URLS of the tweets in the second set of epochs
			for tw2 in list2_type.keys():
				if url in list2_type[tw2]['urls']:
					if "1600daily" not in (resolve_url(url)[1]):

						# Show the tweets with the URL in common
						count += 1
						print("\n" + str(count))
						print(resolve_url(url)[1])
						print("\n" + str(tw) + " -> " + list1_type[tw]['username'] + ": " + list1_type[tw]['text'] + "\n")
						print(str(tw2) + " -> " + list2_type[tw2]['username'] + ": " + list2_type[tw2]['text'] + "\n\n\n")
		

