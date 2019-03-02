import praw
import pdb
import re
import os



#reddit = praw.reddit(client_id, client_secret, user_agent, username, password)
reddit = praw.Reddit(private info)

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





cache = ""



def stob(str = ''):
	binstr = ""
	for c in str:
		i = ord(c)
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
	
def btos(binstr = '', startInd = 0):
	str = ""
	
	index = startInd
	while index < len(binstr):
		num = 0
		for bitno in range(0,8):
			num += (128 / 2**bitno) * (ord(binstr[index + bitno]) - 48);
			#print(ord(binstr[index + bitno])- 48, 128/ 2**bitno)
			#num += 128 * (ord(binstr[index]) - 48);
		
		str += chr(int(num))
		index += 8
		if not index < len(binstr):
			break
		if binstr[index] == ' ':
			index += 1
		
	return str
	
	#for index in range(len(binstr)):
		
def parseBin(binstr = ""):
	index = 0
	noData = bool(1)
	startInd = 0
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
							startInd = index
						noData = bool(0)
						
			else: #only if remaining chars cannot form byte
				#print("not enough for byte")
				index = len(binstr)-1
				break
	if noData:
		return -1
	else: 
		return startInd

#binstr_ = stob("abcdeq")
#print(binstr_)  
#print(("sample text 01101100 01101111 01110010 01100101 01101101\n")) #startInd should be 12
#print("startInd=",parseBin("hfictq01100001"))
#print(parseBin("sample text 01101100 01101111 01110010 01100101 01101101"))
#print(btos(binstr_, 0))

# for every comment on the submission
#for subreddit in reddit.subreddits.popular(limit = 1):
while 1 == 1:
	print("in mentions:\n")
	#print("in submission: ", submission.title)
	#for comment in submission.comments.list():
	#for comment in reddit.inbox.mentions(limit=100):
	for comment in reddit.inbox.unread(mark_read = 1, limit=None):
		author = comment.author
		if bool(1) and comment.body != "[deleted]":
			print("in subreddit r/", comment.subreddit)
			print("by u/", author.name)
			print("comment body:\n ", comment.body)
			# print("submission id=", submission.id)
			# print("comment id=", comment.id)
			# print("parent id=", comment.parent_id)
			print("\n")
		#print("made it past bool")
		if comment.body != "[deleted]":
			if comment.id not in posts_replied_to and "asciicodecbot" not in author.name:
				#print("not yet replied to")
				if re.search("u/asciicodecbot info", comment.body, re.IGNORECASE) and comment.id not in cache:
					comment.reply('You\'ve mentioned ASCIICodecBot!\n\nHere are your options for using my services:\n\n'
								  '   "u/asciicodecbot info": Display list of functions offered.\n'
								  '   "u/asciicodecbot decode": Decodes ascii characters from binary numbers in the parent comment. E.g., "01100001 01100010 011000111 01100100 01100101" would yield "abcde".\n'
								  '   "u/asciicodecbot encode": Encodes ascii characters from parent comment into binary. Like the above function, but backwards.\n'
								  '   "u/asciicodecbot decode this: [some_string]": Decodes ascii characters from binary numbers following "this:"\n'
								  '   "u/asciicodecbot encode this: [some_string]": Encodes ascii characters from parent comment into binary.\n\n"'
								  '**NOTE:** So far, only the "encode" and "decode" functions are working. We\'re working on implementing the other features!\n'
								  'asciicodecbot ver. 0.3');
					cache += comment.id
					posts_replied_to.append(comment.id)
					print("reply sent: info message.")
					
				if re.search("u/asciicodecbot decode", comment.body, re.IGNORECASE) and comment.id not in cache:
					if comment.parent_id == "t3_" + submission.id:
						#parentComment = reddit.comment(comment.parent_id)
						comment.reply("Decoded ASCII text:\n\n" + btos(submission.selftext, parseBin(submission.selftext)))
						cache += comment.id
						posts_replied_to.append(comment.id)
						print("reply sent: text\n")
					else:
						parentComment = comment.parent()
						comment.reply("Decoded ASCII text:\n\n" + btos(parentComment.body, parseBin(parentComment.body)))
						cache += comment.id
						posts_replied_to.append(comment.id)
						print("Reply sent: text\n")			
						
				if re.search("u/asciicodecbot encode", comment.body, re.IGNORECASE) and comment.id not in cache:
					if comment.parent_id == "t3_" + submission.id:
						comment.reply("Encoded ASCII binary:\n\n" + stob(submission.selftext))
						cache += comment.id
						posts_replied_to.append(comment.id)
						print("reply sent: binary\n")
					else:
						parentComment = comment.parent()
						#comment.reply("Encoded ASCII binary:\n\n" + stob(parentComment.body))
						cache += comment.id
						posts_replied_to.append(comment.id)
						print("Reply sent: binary\n")
						
				if re.search("u/asciicodecbot decode this:", comment.body, re.IGNORECASE) and comment.id not in cache:
					#comment.reply("you have mentioned u/asciicodecbot");
					cache += comment.id
					posts_replied_to.append(comment.id)
					print("reply sent: none")
					
				if re.search("u/asciicodecbot encode this:", comment.body, re.IGNORECASE) and comment.id not in cache:
					#comment.reply("you have mentioned u/asciicodecbot");
					cache += comment.id
					posts_replied_to.append(comment.id)
					print("reply sent: none")
	break
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
with open("posts_replied_to.txt", "w") as f:
    for post_id in posts_replied_to:
        f.write(post_id + "\n")