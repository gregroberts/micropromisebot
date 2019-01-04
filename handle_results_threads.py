from db import *
from reddit import *
from content import *

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