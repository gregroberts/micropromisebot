import re
import parsedatetime as pdt 
from datetime import datetime
from db import *
from reddit import *
cal = pdt.Calendar()

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
	elapses_time = cal.parseDT(
		timeframe,
		sourceTime = datetime.fromtimestamp(created_time)
	)[0]
	bot_comment_id = post.reply(body = f'''Youve just made a micropromise!             
	{title}\n\n
elapses at: {elapses_time}\n\n
Here are the pledges to your promise:
	''').id
	c = db.cursor()
	c.execute('''
		INSERT INTO promises
		VALUES
		(?,?,?,?,?,?,?, 1, ?)
	''', 
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
	db.commit()
	c.close()



def handle_plegde(pledge):
	print(f'Handling pledge {pledge}')
	c = db.cursor()
	c.execute('''
		select comment_id from pledges
	''')
	pledges = [i[0] for i in c.fetchall()]
	if pledge[1].id in pledges:
		print('Pledge already handled')
		return None
	c.execute('''
		insert into pledges 
		values
		(?,?,?,?)
	''', 
		(
			pledge[0].id,
			pledge[1].id,
			pledge[1].author.name,
			pledge[1].author.id
		)
	)
	db.commit()
	c.close()
	pledge[1].reply(
		body = 'Thanks for your pledge. You will get a reminder when the promise is due!'
	)
	promise = get_promise(pledge[0].id)
	bot_comment_id = promise[6]
	rt = get_reddit()
	bot_comment = rt.comment(bot_comment_id)
	bot_comment.edit(
		bot_comment.body + '\n\n- /u/' + pledge[1].author.name+'\n'
	)


def handle_watcher(watcher):
	print(f'Handling Watcher {watcher}')
	c = db.cursor()
	c.execute('''
		INSERT INTO watchers
		values
			(?,?,?)
	''', 
		(watcher[0].id,
		watcher[1].author.name,
		 watcher[1].author.id
		 )
	)
	db.commit()
	c.close()

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
