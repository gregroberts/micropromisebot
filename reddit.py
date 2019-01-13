import praw

def get_reddit():
	rt = praw.Reddit('micro')
	return rt

def get_subreddit():
	rt = get_reddit()
	sb = rt.subreddit('micropromise')
	return sb

def get_new_posts(limit=10):
	print('getting new posts')
	s = get_subreddit()
	return list(s.new(limit=limit))


def get_promise_posts():
	mp = get_subreddit()
	promise_posts = mp.search('title:\[promise\]')
	return [
		i for i in promise_posts
		if '[promise]' in i.title.lower()
		and str(i.link_flair_text) !='ELAPSED'
	]


def get_results_posts():
	print(' get_results_posts')
	mp = get_subreddit()
	results_posts = mp.search('title:[results]')
	return [
		i for i in results_posts
		if '[results]' in i.title.lower()
		and str(i.link_flair_text) !='ELAPSED'
	]


def get_all_promise_comments():
	all_comments = []
	for post in get_promise_posts():
		for comment in post.comments:
			all_comments.append((post,comment))
	return all_comments


def get_all_watch_comments():
	watch_comments = []
	for i in get_all_promise_comments():
		if i[1].body.lower().startswith('[watch]') \
		or i[1].body.lower().startswith('\[watch\]'):
			watch_comments.append(i)
	return watch_comments


def get_all_pledge_comments():
	pledge_comments = []
	for i in get_all_promise_comments():
		if i[1].body.lower().startswith('[pledge]') \
		or i[1].body.lower().startswith('\[pledge\]') :
			pledge_comments.append(i)
	return pledge_comments




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
		if i[1].body.lower().startswith('[kept]')\
		or i[1].body.lower().startswith('\[kept\]'):
			kept_comments.append(i)
	return kept_comments