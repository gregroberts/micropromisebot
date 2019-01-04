import praw, imp, sqlite3, re
import parsedatetime as pdt 
from datetime import datetime
from db import *
from reddit import *
cal = pdt.Calendar()

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
Back on {created_time}, /u/{promiser_id} made a micropromise:

[{promise_title}]({original_post_link})

They got {n_pledges} pledges, from:\n\n
/u/{pledgerss}

How did they do?\n\n
'''
	results_thread = rt.subreddit('micropromise').submit(
		f'[RESULTS] {promise_title}',
		selftext = results_thread_body
	)
	rt.redditor(promiser_id).message(
		f'Micropromise reminder {promise_body}',
		f'''
Hey! Your promise '{promise_title}' has expired.
Come join us in the results thread:
https://www.reddit.com/r/micropromise/comments/{results_thread.id}/

and write a comment starting with [KEPT] to tell us you succeeded.
Didn't succeed? Don't worry about it! We all have stuff going on, 
what's important is you're thinking on the right track.

Feel free to start a new promise thread and keep the dream alive!
		'''
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
	get_finished_promises()
	handle_all_results_threads()