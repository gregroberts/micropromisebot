import re
import parsedatetime as pdt 
from datetime import datetime
from db import *
from reddit import *
from content import *


def handle_promise(post):
	print(f'Handling promise {post}')
	existent_promises = [i[0] for i in get_existent_promise_ids()]
	if post.id in existent_promises:
		print('Promise already exists')
		return None
	print(f'Handling new promise {post}, {post.title}')
	_id = post.id
	title = post.title
	user_id = post.author.id
	user_name = post.author.name
	created_time = post.created_utc
	timeframe =  ','.join(re.findall('\[\w+] \[(.*)\]', title))
	print(datetime.fromtimestamp(created_time))
	cal = pdt.Calendar()
	elapses_time = cal.parseDT(
		timeframe,
		sourceTime = datetime.fromtimestamp(created_time)
	)[0]
	bot_comment_id = comment_promise(post, title, elapses_time)
	insert_promise(
		(
			_id,
			title,
			user_id,
			created_time,
			timeframe,
			elapses_time.timestamp(),
			bot_comment_id,
			user_name
		)
	)



def handle_all_promises():
	print('handling all promises')
	for post in get_promise_posts():
		handle_promise(post)
		
if __name__ == '__main__':	
	handle_all_promises()
