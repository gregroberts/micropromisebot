from reddit import get_reddit
from templates import *
rt = get_reddit()


def comment_promise(post, title, elapses_time):
	bot_comment_id = post.reply(body = PROMISE_COMMENT_BODY.format(**locals())).id
	return bot_comment_id

def comment_pledge(pledger):
	pledger.reply(
		body = 'Thanks for your pledge. You will get a reminder when the promise is due!'
	)

def post_results_thread(promiser_id, created_time, promise_title, pledgers, promise):
	n_pledges = len(pledgers)
	pledgerss = '\n,- /u/'.join(
		[i[2] for i in pledgers]
	)
	original_post_link = f'https://www.reddit.com/r/micropromise/comments/{promise[0]}/'
	results_thread_body = RESULTS_THREAD_BODY.format(**locals())
	results_thread = rt.subreddit('micropromise').submit(
		f'[RESULTS] {promise_title}',
		selftext = results_thread_body
	)
	return results_thread

def message_promiser(promise_title, results_thread_id, promiser_id, promise_body):
	rt.redditor(promiser_id).message(
                f'Micropromise reminder {promise_title}'[:94]+'...',
		PROMISE_MESSAGE_BODY.format(**locals())
	)

def message_pledger(pledger_id, promiser_id, promise_title, results_thread_id):
	rt.redditor(pledger_id).message(
                f'Micropromise reminder {promise_title}'[:94]+'...',
		PLEDGE_MESSAGE_BODY.format(**locals())
	)

def message_watcher(watcher_id, promiser_id, promise_title, results_thread_id):
	rt.redditor(watcher_id).message(
                f'Micropromise reminder {promise_title}'[:94]+'...',
		WATCHER_MESSAGE_BODY.format(**locals())
	)
