from reddit import *
from db import *


def check_promise_result(results_thread):
	promises_to_check = get_promises_to_check()
	for i in promises_to_check:
		if i[0] in results_thread.selftext:
			print(i[0],i[1])
			print(results_thread.selftext)
			kept = 0
			if i[1] in results_thread.selftext:
				kept = 1
				print('Promise Kept!')
			update_kept_promise(i[0], kept)


def check_pledge_result(results_thread):
	pledges_to_check = get_pledges_to_check()
	for i in pledges_to_check:
		if i[0] in results_thread.selftext:
			print(i[0],i[1])
			print(results_thread.selftext)
			if i[1] in results_thread.selftext:
				print('Pledge Kept!')
				update_kept_pledge(i[2])


def check_promise_keepers():
	for i in get_results_posts():
		check_promise_result(i)
		check_pledge_result(i)


if __name__ == '__main__':
	check_promise_keepers()