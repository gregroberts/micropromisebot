from time import time
from reddit import *
from db import *


def mark_promises_as_expired():
	promise_posts = get_promise_posts()
	expired_promises = get_expired_promises()
	expired_ids = set(i[0] for i in expired_promises)
	for promise_post in promise_posts:
		if promise_post.id in expired_ids:
			print(f'EXPIRED: {promise_post.title}')
			promise_post.mod.flair(text='PROMISE|ELAPSED')
		else:
			print(f'NOT EXPIRED: {promise_post.title}')


def mark_results_as_expired():
	results_posts = get_results_posts()
	now = time()
	two_days_ago = now - 2*24*3600
	for results_post in results_posts:
		if results_post.created_utc < two_days_ago:
			print(f'EXPIRED: {results_post.title}')
			results_post.mod.flair(text='RESULTS|ELAPSED')
		else:
			print(f'NOT EXPIRED: {results_post.title}')




if __name__ == '__main__':
	mark_results_as_expired()
