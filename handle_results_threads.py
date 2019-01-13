import re
from db import *
from reddit import *
from content import *

def handle_results_comments(results_thread):
	#print(' handle_results_comments')
	kept_comments = get_all_kept_comments(results_thread)
	promise_id = ''.join(re.findall(
		'micropromise/comments/(.*)/',
		results_thread.selftext
	))
	promise = get_promise(promise_id)
	promiser = ''
	if promise:
		promiser = promise[8]
	for i in kept_comments:
		author = i[1].author.name
		un = '/u/'+author+' kept their promise!'
		if author == promiser:
			extend_post_flair(results_thread, ['KEPT'])
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