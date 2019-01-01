import praw, imp, sqlite3, re
import parsedatetime as pdt 
from datetime import datetime

cal = pdt.Calendar()

db = sqlite3.connect('micropromise.db')
c = db.cursor()
c.execute('''
	CREATE TABLE IF NOT EXISTS
		promises 
		(
			id text,
			title text,
			user_id text,
			created_time int,
			timeframe text,
			elapses_time int,
			bot_comment_id text,
			live int default 1,
			user_name text
		)
''')
c.execute('''
	CREATE TABLE IF NOT EXISTS pledges
	(
		promise_id text,
		comment_id text,
		user_name text,
		user_id text
	)
''')
c.execute('''
	CREATE TABLE IF NOT EXISTS watchers
	(
		promise_id text,
		user_name text,
		user_id text
	)
''')
db.commit()
c.close()

def get_reddit():
	rt = praw.Reddit('micro')
	return rt

def get_new_posts(limit=10):
	print('getting new posts')
	rt = get_reddit()
	s=rt.subreddit('micropromise')
	return list(s.new(limit=limit))

def get_existent_promise_ids():
	print('getting existing promises')
	c = db.cursor()
	c.execute('SELECT id from promises')
	data = c.fetchall()
	c.close()
	return data

def get_promise_posts():
	promise_posts = []
	for i in get_new_posts(50):
		print(i.title)
		if i.title.lower().startswith('[promise]'):
			promise_posts.append(i)
	return promise_posts

def get_promise(id):
	c = db.cursor()
	print(id)
	c.execute(f'''
		select * from promises 
		where id = '{id}'
		'''
	)
	data = c.fetchone()
	print(data)
	return data

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


def get_all_promise_comments():
	all_comments = []
	for post in get_promise_posts():
		for comment in post.comments:
			all_comments.append((post,comment))
	return all_comments


def get_all_pledge_comments():
	pledge_comments = []
	for i in get_all_promise_comments():
		print(i[1].body)
		if i[1].body.lower().startswith('[pledge]') \
		or i[1].body.lower().startswith('\[pledge\]') :
			print('pledge!')
			pledge_comments.append(i)
	return pledge_comments

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
		body = 'Thanks for your plegde. You will get a reminder when the promise is due!'
	)
	promise = get_promise(pledge[0].id)
	bot_comment_id = promise[6]
	rt = get_reddit()
	bot_comment = rt.comment(bot_comment_id)
	bot_comment.edit(
		bot_comment.body + '\n\n- /u/' + pledge[1].author.name+'\n'
	)

def get_all_watch_comments():
	watch_comments = []
	for i in get_all_promise_comments():
		print(i[1].body)
		if i[1].body.lower().startswith('[watch]') \
		or i[1].body.lower().startswith('\[watch\]'):
			print('watch!')
			watch_comments.append(i)
	return watch_comments

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

def get_promise_pledges(promise_id):
	c = db.cursor()
	c.execute(f'''
		select * from pledges
		where promise_id = '{promise_id}'
	''')
	pledgers = c.fetchall()
	c.close()
	return pledgers

def get_promise_watchers(promise_id):
	c = db.cursor()
	c.execute(f'''
		select * from watchers
		where promise_id = '{promise_id}'
	''')
	watchers = c.fetchall()
	c.close()
	return watchers

def finish_promise(promise):
	rt = get_reddit()
	c = db.cursor()
	#make results thread
	promise_body = promise[1]
	promise_title = promise_body.split(']')[-1]
	promiser = promise[2]
	promiser_id = promise[8]
	created_time = datetime.fromtimestamp(promise[3])
	pledgers = get_promise_pledges(promise[0])
	n_pledges = len(pledgers)
	pledgerss = '\n,- /u/'.join(
		[i[2] for i in pledgers]
	)
	original_post_link = f'https://www.reddit.com/r/micropromise/comments/{promise[0]}/'
	results_thread_body = f'''
Back on {created_time}, {promiser_id} made a micropromise:

[{promise_title}]({original_post_link})

They got {n_pledges} pledges, from:\n\n
{pledgerss}

How did they do?\n\n
'''
	results_thread = rt.subreddit('micropromise').submit(
		f'[RESULTS] {promise_title}',
		selftext = results_thread_body
	)
	#notify pledgers
	for i in pledgers:
		pledger_id = i[2]
		print(pledger_id)
		rt.redditor(pledger_id).message(
			f'Micropromise reminder {promise_body}',
			f'''You kindly pledged to help {promiser_id} with their promise.
Come and contribute to the results thread here:
	https://www.reddit.com/r/micropromise/comments/{results_thread.id}/

And/or reply to this message to let us know how you did!
			'''
			)
	#notify watchers
	print('notifying watchers')
	watchers = get_promise_watchers(promise[0])
	for i in watchers:
		print(i)
		watcher_id = i[1]
		rt.redditor(watcher_id).message(
			f'Micropromise reminder {promise_body}',
			f'''You Asked to watch {promiser_id} and their promise on /r/micropromise.
Check out the results thread here:
	https://www.reddit.com/r/micropromise/comments/{results_thread.id}/
			'''
		)
	c.execute(f'''
		update promises
		set live = 0 
		where id = '{promise[0]}'
	''')
	db.commit()
	c.close()

def get_finished_promises():
	c = db.cursor()
	c.execute('''
		select * from promises
		where live = 1
		and datetime(elapses_time,\'unixepoch\')<datetime(\'now\')
			
	''')
	finished_promises = c.fetchall()
	print(
		f'Found {len(finished_promises)} finished promises'
	)
	for i in finished_promises:
		finish_promise(i)

def get_results_posts():
	print(' get_results_posts')
	results_posts = []
	for i in get_new_posts(50):
		print(i.title)
		if i.title.lower().startswith('[results]'):
			results_posts.append(i)
	return results_posts

def get_all_results_comments(results_thread):
	print(' get_all_results_comments')
	all_comments = []
	for comment in results_thread.comments:
		all_comments.append((results_thread,comment))
	return all_comments


def get_all_kept_comments(results_thread):
	print(' get_all_kept_comments')
	kept_comments = []
	for i in get_all_results_comments(results_thread):
		print(i[1].body)
		if i[1].body.lower().startswith('[kept]')\
		or if i[1].body.lower().startswith('\[kept\]'):
			print('kept!')
			kept_comments.append(i)
	return kept_comments

def handle_results_comments(results_thread):
	print(' handle_results_comments')
	kept_comments = get_all_kept_comments(results_thread)
	for i in kept_comments:
		author = i[1].author.name
		un = '/u/'+author+' kept their promise!'
		if un in results_thread.selftext:
			continue
		if author not in results_thread.selftext:
			continue
		else:
			results_thread.edit(
				results_thread.selftext + '\n\n'+un
			)

def handle_all_results_threads():
	print(' handle_all_results_threads')
	for i in get_results_posts():
		handle_results_comments(i)

if __name__ == '__main__':
	handle_all_results_threads()
	get_finished_promises()
	handle_all_posts()