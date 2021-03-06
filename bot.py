import praw
import config
from yagmail import SMTP, inline
import sys
import time



# Logs the bot into Reddit
def bot_login():
	print("Logging in")
	r = praw.Reddit(username = config.username,
					password = config.password,
					client_id = config.client_id,
					client_secret = config.client_secret,
					user_agent = "Test bot to send emails to self")
	print("Logged in")
	return r

# Return true or false depending on if input post matches the designated post
def correct_post(input_title):
	designated_post = "Pick of the Day"
	correct_title = designated_post.split(" ")

	for index in range (0, 4):
		if input_title[index] != correct_title[index]:
			return False

	return True

def print_border():
	print("\n\n--------------------------------------------------------")
	print("--------------------------------------------------------\n\n")


# Run the actual bot
def run_bot(r):

	reload(sys);
	sys.setdefaultencoding("utf8")

	# Change authors below to add/remove which authors you want 
	# The second value is their latest comment
	selected_authors = {'Ndborro': None, 'lyyphe2': None}

	subreddit = r.subreddit('sportsbook')

	while True:

		time.sleep(60*5)
		
		for submission in subreddit.new(limit=12):

	  		sub_title = submission.title  # Output: the submission's title
	   		sub_title_list_form = sub_title.split(" ")

	   		if correct_post(sub_title_list_form):

   				for comment in submission.comments:
   					if comment.author in selected_authors.keys():
   						# Checks if there is a new post
   						if selected_authors.get(comment.author) != comment:
   							print_border()
   							print("New post detected - Sending Email\n")
							print "Author: ",
							print(comment.author)
	   						send_email(sub_title, comment.body, comment.author)
	   						print("\nEmail sent")
	   						print_border()
	   						selected_authors[comment.author] = comment	

   			
def send_email(title, body, author):
	yag = SMTP('bryce1234sendredditupdates@gmail.com')
	contents = [body]
	date = time.strftime("%d/%m/%Y")
	title = "POTD "+date
	yag.send('bryce1234sendredditupdates@gmail.com', title, contents)


run_bot(bot_login())



