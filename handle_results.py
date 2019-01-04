import praw, re
from datetime import datetime
from db import *
from reddit import *
from content import *

def finish_promise(promise):
	#make results thread
	promise_body = promise[1]
	promise_title = promise_body.split(']')[-1]
	promiser = promise[2]
	promiser_id = promise[8]
	created_time = datetime.fromtimestamp(promise[3])
	pledgers = get_promise_pledges(promise[0])
	results_thread = post_results_thread(
		promiser_id, 
		created_time, 
		promise_title, 
		pledgers,
		promise
	)
	message_promiser(
		promise_title, 
		results_thread.id,
		promiser_id,
		promise_title,
	)
	#notify pledgers
	for i in pledgers:
		pledger_id = i[2]
		print(pledger_id)
		message_pledger(
			pledger_id,
			promiser_id, 
			promisetitle,
			results_thread_id
		)
	#notify watchers
	print('notifying watchers')
	watchers = get_promise_watchers(promise[0])
	for i in watchers:
		print(i)
		watcher_id = i[1]
		message_watcher(
			watcher_id,
			promiser_id,
			promise_title,
			results_thread_id
		)
	update_finished_promise(promise[0])

def finish_all_promises():
	finished_promises = get_finished_promises()
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
	finish_all_promises()
	handle_all_results_threads()