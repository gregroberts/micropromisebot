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


def handle_plegde(pledge):
	print(f'Handling pledge {pledge}')
	pledges = get_pledges()
	if pledge[1].id in pledges:
		print('Pledge already handled')
		return None
	insert_pledge(
		(
			pledge[0].id,
			pledge[1].id,
			pledge[1].author.name,
			pledge[1].author.id
		)
	)
	comment_pledge(pledge[1])
	promise = get_promise(pledge[0].id)
	bot_comment_id = promise[6]
	rt = get_reddit()
	bot_comment = rt.comment(bot_comment_id)
	bot_comment.edit(
		bot_comment.body + '\n\n- /u/' + pledge[1].author.name+'\n'
	)


def handle_watcher(watcher):
	print(f'Handling Watcher {watcher}')
	insert_watcher(
		(
			watcher[0].id,
			watcher[1].author.name,
			watcher[1].author.id
		 )
	)

def handle_all_promises():
	print('handling all promises')
	for post in get_promise_posts():
		handle_promise(post)

def handle_all_pledges():
	print('handling all pledges')
	for pledge in get_all_pledge_comments():
		handle_plegde(pledge)

def handle_all_watchers():
	print('handling all watchers')
	for watcher in get_all_watch_comments():
		handle_watcher(watcher)

def handle_all_posts():
	print('handling all posts')
	handle_all_promises()
	handle_all_pledges()
	handle_all_watchers()


if __name__ == '__main__':	
	handle_all_posts()
