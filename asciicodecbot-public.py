import sys
import praw
import pdb
import re
import os
import datetime
import time



#reddit = praw.reddit(client_id, client_secret, user_agent, username, password)
reddit = praw.Reddit(client_id='data_expunged', client_secret='data_expunged', user_agent='ascii codec bot', username='ASCIICodecBot', password='data_expunged')

submission = reddit.submission(url='https://www.reddit.com/r/BotTestingPlace/comments/avnv6z/bot_testing_submission_2/')
#submission = reddit.submission(url='https://www.reddit.com/r/BotTestingPlace/comments/avys09/encode/')
#submission = reddit.submission(url='https://www.reddit.com/r/asskreddit/comments/avyp63/whats_your_craziest_drug_story/')
submission = reddit.submission(url='https://www.reddit.com/r/bottestingplace/comments/awc40x/testing_place_3/')
#submission.reply("test message two");


if not os.path.isfile("posts_replied_to.txt"):
    posts_replied_to = []
else:
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = list(filter(None, posts_replied_to))
		
if not os.path.isfile("posts_seen.txt"):
    posts_seen = []
else:
    with open("posts_seen.txt", "r") as f:
        posts_seen = f.read()
        posts_seen = posts_seen.split("\n")
        posts_seen = list(filter(None, posts_seen))
cache = ""




def stox(str = "", start_ind = 0):
	hexstr = ""
	if start_ind < 0:
		return ""
	for c in range(start_ind, len(str)):
		i = ord(str[c])
		j = i - i % 16
		j = int(j / 16) # j is now representative of first hex digit
		if j < 10:
			hexstr += chr(j + 48)
		elif j < 16:
			hexstr += chr(j + 55)
		else:
			hexstr += '0'
		
		i -= j * 16 # i is second hex digit
		if i < 10:
			hexstr += chr(i + 48)
		elif i < 16:
			hexstr += chr(i + 55)
		else:
			hexstr += '0'
		
		hexstr += ' '
	return hexstr

def xtos(hexstr = "", start_ind = 0):
	str = ""
	if start_ind < 0:
		return ""
	index = start_ind
	while len(hexstr) - index >= 2:
		num = int(0)
		#for bitno in range(0, 2):
		
		character = ord(hexstr[index + 0])
		if 48 <= character and character <= 57:
			num += (character - 48) * 16
		elif 65 <= character and character <= 70:
			num += (character - 55) * 16
		
		character = ord(hexstr[index + 1])
		if 48 <= character and character <= 57:
			num += (character - 48) * 1
		elif 65 <= character and character <= 70:
			num += (character - 55) * 1
		
		#num += (128 / 2**bitno) * (ord(hexstr[index + bitno]) - 48)
		#print(ord(binstr[index + bitno])- 48, 128/ 2**bitno)
		#num += 128 * (ord(binstr[index]) - 48);
		str += chr(int(num))
		index += 2
		if index >= len(hexstr):
			break
		if hexstr[index] == ' ':
			index += 1
		
	return str

def parse_hex(hexstr = "", start_ind = 0):
	index = start_ind
	noData = True
	#start_ind = 0
	character = ''
	#num = 1
	while index < len(hexstr):
		#print("index=", index)
		if not noData:
			break
			
		character = ord(hexstr[index])
		if not ((48 <= character and character <= 57) or (65 <= character and character <= 70)): # if not a hex digit
			#print("no x")
			index += 1
		else: # if yes hex digit
			#print("yes x")
			if len(hexstr) - index >= 2: # if remaining chars can form a byte
				#print("enough chars for byte")
				for charno in range(0,2):
					character = ord(hexstr[index + charno])
					if not ((48 <= character and character <= 57) or (65 <= character and character <= 70)): #if not hex digit
						#print("not a hex")
						index += charno + 1# increment index by bit number
						break
					#else: #if it is hex
						#print("yes x")
						#print("charno=",charno)
						#print(noData)
						#do nothing
					if charno == 1:
						#code
						
						if noData:
							start_ind = index
						noData = False
						
			else: #only if remaining chars cannot form byte
				#print("not enough for byte")
				index = len(hexstr)-1
				break
			index += 2
	if noData:
		return -1
	else: 
		return start_ind
	str = ""
	if start_ind < 0:
		return ""
	index = start_ind
	while index < len(binstr):
		num = int(0)
		for bitno in range(0, 8):
			num += (128 / 2**bitno) * (ord(binstr[index + bitno]) - 48);
			#print(ord(binstr[index + bitno])- 48, 128/ 2**bitno)
			#num += 128 * (ord(binstr[index]) - 48);
		str += chr(int(num))
		index += 8
		if index >= len(binstr):
			break
		if binstr[index] == ' ':
			index += 1
		
	return str

def stob(str = "", start_ind = 0):
	binstr = ""
	if start_ind < 0:
		return ""
	for c in range(start_ind, len(str)):
		i = ord(str[c])
		for counter in range(8):
			if (i >= 128): # if even
				binstr = binstr + '1'
			else:
				binstr = binstr + '0'
			i = i << 1 # left shift i
			if i > 255:
				i -= 256
		binstr = binstr + ' '
	return binstr
	
def btos(binstr = "", start_ind = 0):
	str = ""
	if start_ind < 0:
		return ""
	index = start_ind
	while index < len(binstr):
		num = int(0)
		for bitno in range(0, 8):
			num += (128 / 2**bitno) * (ord(binstr[index + bitno]) - 48);
			#print(ord(binstr[index + bitno])- 48, 128/ 2**bitno)
			#num += 128 * (ord(binstr[index]) - 48);
		str += chr(int(num))
		index += 8
		if index >= len(binstr):
			break
		while binstr[index] == ' ' or binstr[index] == '\n':
			index += 1
		
	return str
		
def parse_bin(binstr = ""):
	index = 0
	noData = True
	start_ind = 0
	#num = 1
	while index < len(binstr):
		#print("index=", index)
		if not noData:
			break
		if not (binstr[index + 0] == '0' or binstr[index + 0] == '1'): # if neither 1 nor 0
			index += 1
		else: # if yes 1 or 0
			if len(binstr) - index >= 8: # if remaining chars can form a byte
				#print("enough chars for byte")
				for charno in range(0,8):
					if not (binstr[index + charno] == '0' or binstr[index + charno] == '1'): #if neither 0 nor 1, for each char
						#print("not a bit")
						index += charno + 1# shift index right by bit number
						break
					#else: #if it is either 1 or 0
						#print("yes bit")
						#print(charno)
						#do nothing
					if charno == 7:
						#code
						
						if noData:
							start_ind = index
						noData = False
						
			else: #only if remaining chars cannot form byte
				#print("not enough for byte")
				index = len(binstr)-1
				break
	if noData:
		return -1
	else: 
		return start_ind
		
# for every comment on the submission
#for subreddit in reddit.subreddits.popular(limit = 1):

if len(sys.argv) > 1:
	time_interval = int(sys.argv[1])
else:
	time_interval = 30

post_is_deleted = False
starting_timestamp = int(time.time())
#time_interval = 30
service_requested = ""
iterations = 0

if time_interval < 1:
	time_interval = 30

while True:
	reply_qty = 0
	iterations += 1
	try:
		while time.time() % time_interval > 0.5:
			sys.stdout.write("\r%02d seconds until refresh..." % (time_interval - time.time() % time_interval))
			sys.stdout.flush()
			time.sleep(0.5)
	except:
		print(reply_qty, '\n')
		raise
	
	print("\n%d\niteration %d\n" % (int(time.time()), iterations))
	print("****In mentions:****\n")
	
	#print("in submission: ", submission.title)
	#for comment in submission.comments.list():
	#for comment in reddit.inbox.mentions(limit=100):
	for comment in reddit.inbox.unread(mark_read = True, limit = None):
		if comment.id not in posts_replied_to and comment.id not in posts_seen and re.search("u/asciicodecbot", comment.body, re.IGNORECASE):
			author = comment.author
			submission = comment.submission
			
			if comment.body != "[deleted]":
				print("in r/%s" % comment.subreddit)
				print("by u/%s" % author.name)
				# print("submission id =", submission.id)
				# print("comment id=", comment.id)
				print("comment body:\n\n%s\n" % (comment.body))
				
				# print("parent id=", comment.parent_id)
				#print("made it past bool")
			replySent = False
			
			# post_is_deleted = False
			# if comment.parent_id == "t3_" + submission.id: #top-level comment
				# if submission.selftext != "[deleted]":
					# post_is_deleted = True
			# else:
				# if comment.parent.body != "[deleted]":
					# post_is_deleted = True
			
			
			if not post_is_deleted:
				try:
					if "asciicodecbot" not in author.name:
						
						service_requested = "none"
						if re.search("u/asciicodecbot info", comment.body, re.IGNORECASE) or re.search("u/asciicodecbot help", comment.body, re.IGNORECASE):
							service_requested = "info"
						if re.search("u/asciicodecbot decode", comment.body, re.IGNORECASE):
							service_requested = "decode"
						if re.search("u/asciicodecbot decode hex", comment.body, re.IGNORECASE):
							service_requested = "xdecode"
						if re.search("u/asciicodecbot encode", comment.body, re.IGNORECASE):
							service_requested = "encode"
						if re.search("u/asciicodecbot encode hex", comment.body, re.IGNORECASE):
							service_requested = "xencode"
						if re.search("u/asciicodecbot decode:", comment.body, re.IGNORECASE):
							service_requested = "dthis"
						if re.search("u/asciicodecbot decode hex:", comment.body, re.IGNORECASE):
							service_requested = "xdthis"
						if re.search("u/asciicodecbot encode:", comment.body, re.IGNORECASE):
							service_requested = "ethis"
						if re.search("u/asciicodecbot encode hex:", comment.body, re.IGNORECASE):
							service_requested = "xethis"
						
						if comment.id not in cache:
							if service_requested == "info":
								comment.reply('You\'ve mentioned ASCIICodecBot!\n\nHere are your options for using my services:\n***\n'
											  '   "u/asciicodecbot info": Display list of functions offered.\n\n'
											  '   "u/asciicodecbot decode": Decodes ascii characters from binary numbers in the parent comment. E.g., "01100001 01100010 011000111 01100100 01100101" would yield "abcde".\n\n'
											  '   "u/asciicodecbot encode": Encodes ascii characters from parent comment into binary. Like the above function, but backwards.\n\n'
											  '   "u/asciicodecbot decode: [some_string]": Decodes ascii characters from binary numbers following "this:"\n\n'
											  '   "u/asciicodecbot encode: [some_string]": Encodes ascii characters from parent comment into binary.\n\n'
											  '   Follow the keywords "encode" or "decode" with "hex" to test out the new hexadecimal feature!\n***\n'
											  '^(asciicodecbot ver. 0.7 | created by u/Nissingmo)')
								cache += comment.id
								posts_replied_to.append(comment.id)
								replySent = True
								print("reply sent: info message.")
								
							if service_requested == "decode":
								if comment.parent_id.find("t3_", 0) == 0:
									#parentComment = reddit.comment(comment.parent_id)
									#print("submission selftext:\n\n", submission.selftext)
									comment.reply("Decoded ASCII text:\n\n" + btos(submission.selftext, parse_bin(submission.selftext)))
									cache += comment.id
									posts_replied_to.append(comment.id)
									replySent = True
									print("reply sent: text\n")
								else:
									parentComment = comment.parent()
									comment.reply("Decoded ASCII text:\n\n" + btos(parentComment.body, parse_bin(parentComment.body)))
									cache += comment.id
									posts_replied_to.append(comment.id)
									replySent = True
									print("Reply sent: text\n")			
									
							if service_requested == "xdecode":
								if comment.parent_id.find("t3_", 0) == 0:
									#parentComment = reddit.comment(comment.parent_id)
									comment.reply("Decoded ASCII text:\n\n" + btos(submission.selftext, parse_bin(submission.selftext)))
									cache += comment.id
									posts_replied_to.append(comment.id)
									replySent = True
									print("reply sent: text\n")
								else:
									parentComment = comment.parent()
									if re.search("encoded ascii hexadecimal:", parentComment.body, re.IGNORECASE):
										offset = 26
									else:
										offset = 0
									comment.reply("Decoded ASCII text:\n\n" + xtos(parentComment.body, parse_hex(parentComment.body, offset)))
									cache += comment.id
									posts_replied_to.append(comment.id)
									replySent = True
									print("Reply sent: text\n")	
							
							if service_requested == "encode":
								if comment.parent_id.find("t3_", 0) == 0:
									comment.reply("Encoded ASCII binary:\n\n" + stob(submission.selftext))
									cache += comment.id
									posts_replied_to.append(comment.id)
									replySent = True
									print("reply sent: binary\n")
								else:
									parentComment = comment.parent()
									comment.reply("Encoded ASCII binary:\n\n" + stob(parentComment.body))
									cache += comment.id
									posts_replied_to.append(comment.id)
									replySent = True
									print("Reply sent: binary\n")
									
							if service_requested == "xencode":
								if comment.parent_id.find("t3_", 0) == 0:
									comment.reply("Encoded ASCII hexadecimal:\n\n" + stox(submission.selftext))
									cache += comment.id
									posts_replied_to.append(comment.id)
									replySent = True
									print("reply sent: hex\n")
								else:
									parentComment = comment.parent()
									comment.reply("Encoded ASCII hexadecimal:\n\n" + stox(parentComment.body))
									cache += comment.id
									posts_replied_to.append(comment.id)
									replySent = True
									print("Reply sent: hex\n")
									
							if service_requested == "dthis":	
								index_found = comment.body.lower().find("u/asciicodecbot decode:") + 22
								comment.reply("Decoded inline ASCII text:\n\n" + btos(comment.body, parse_bin(comment.body, index_found)))
								cache += comment.id
								posts_replied_to.append(comment.id)
								replySent = True
								print("reply sent: inline text\n\n")
							
							if service_requested == "xdthis":
								index_found = comment.body.lower().find("u/asciicodecbot decode hex:") + 26
								comment.reply("Decoded inline ASCII text:\n\n" + xtos(comment.body, parse_hex(comment.body, index_found)))
								cache += comment.id
								posts_replied_to.append(comment.id)
								replySent = True
								print("reply sent: inline text\n\n")
								
							if service_requested == "ethis":
								#comment.reply("you have mentioned u/asciicodecbot");
								index_found = comment.body.lower().find("u/asciicodecbot encode this:") + 28
								# while not (comment.body[index_found] == '1' or comment.body[index_found] == '0') and index_found < len(comment.body):
									# index_found += 1
								comment.reply("Encoded inline ASCII binary:\n\n" + stob(comment.body, index_found))
								cache += comment.id
								posts_replied_to.append(comment.id)
								replySent = True
								print("reply sent: inline binary\n\n")
							
							if service_requested == "xethis":
								#comment.reply("you have mentioned u/asciicodecbot");
								index_found = comment.body.lower().find("u/asciicodecbot encode hex:") + 27
								# while not (comment.body[index_found] == '1' or comment.body[index_found] == '0') and index_found < len(comment.body):
									# index_found += 1
								comment.reply("Encoded inline ASCII hexadecimal:\n\n" + stox(comment.body, index_found))
								cache += comment.id
								posts_replied_to.append(comment.id)
								replySent = True
								print("reply sent: inline hex\n\n")
							
						if replySent:
							reply_qty += 1
						else:
							print("no reply sent: no valid service requested\n\n")
					else:
						print("no reply sent: comment posted by u/asciicodecbot\n\n")
				except KeyboardInterrupt:
					print(reply_qty, "replies sent\n\n")
					#raise
				except:
					print("No reply sent: exception occurred:\n", sys.exc_info()[0])
					#raise
			else:
				print("no reply sent: post is deleted\n\n")
		posts_seen.append(comment.id)
		
	with open("posts_replied_to.txt", "w") as f:
		for post_id in posts_replied_to:
			f.write(post_id + "\n")
	with open("posts_seen.txt", "w") as f:
		for post_id in posts_seen:
			f.write(post_id + "\n")
	print("%d replies sent.\n****    Done    ****\n\n\n" % reply_qty)
	#break #only break for manual operation
#comment


# # Create a list
# if not os.path.isfile("posts_replied_to.txt"):
    # posts_replied_to = []

# # Or load the list of posts we have replied to
# else:
    # with open("posts_replied_to.txt", "r") as f:
        # posts_replied_to = f.read()
	# posts_replied_to = posts_replied_to.split("\n")
		# posts_replied_to = list(filter(None, posts_replied_to))

		# # Pull the hottest 10 entries from a subreddit of your choosing
# subreddit = reddit.subreddit('BotTestingPlace')
# for submission in subreddit.new(limit=1):
    # #print(submission.title)

    # # Make sure you didn't already reply to this post
    # if submission.id not in posts_replied_to:

        # # Not case sensitive
        # if re.search("asciicodecbot", submission.title, re.IGNORECASE):
            # # Reply
            # submission.reply("this is a test message.")
            # print("Bot replying to : ", submission.title)

            # # Store id in list
            # posts_replied_to.append(submission.id)

# # Write updated list to file
