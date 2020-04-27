import json
from os import listdir
from os.path import isfile, join

# Get all of the files within a given directory
onlyfiles = [f for f in listdir("projectdata/jan-epoch2") if isfile(join("projectdata/jan-epoch2", f))]
list_of_files = []

# Add only core dataset files within the directory to list_of_files
for i in onlyfiles:
	if i[-5:] == ".json" and i[:2] != "._":
		print(i)
		list_of_files.append(i)

print("\n\n\n")
unique_ids = []

# Open uniqueids.txt in the folder you're working on, ready to add all tweet_ids from the dataset
with open("projectdata/jan-epoch2/uniqueids.txt", "w") as unique_ids_doc:
	for i in list_of_files:
		print("Working on: " + i)
		# Open each file within the directory
		with open(("projectdata/jan-epoch2/" + i), "r") as json_file:

			# For each tweet, write their unique tweet_id into the uniqueids.txt file
			count = 0
			for tw in json_file:
				count += 1
				if count % 20000 == 0:
					print(str(count))
				tweet = json.loads(tw)
				id = tweet['id']
				unique_ids_doc.write(str(id)+"\n")
			





