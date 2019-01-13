from db import *
from reddit import *
from content import *


def handle_plegde(pledge):
	print(f'Handling pledge {pledge}')
	pledges = get_pledges()
	if pledge[1].id in pledges:
		print('Pledge already handled')
		return None
	promise = get_promise(pledge[0].id)
	if promise is None:
		print('Promise no exist')
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


def handle_all_pledges():
	print('handling all pledges')
	for pledge in get_all_pledge_comments():
		handle_plegde(pledge)

def handle_all_watchers():
	print('handling all watchers')
	for watcher in get_all_watch_comments():
		handle_watcher(watcher)


if __name__ == '__main__':
	handle_all_watchers()
	handle_all_pledges()
