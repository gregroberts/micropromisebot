PROMISE_COMMENT_BODY = '''Youve just made a micropromise!             
	{title}\n\n
elapses at: {elapses_time}\n\n
Here are the pledges to your promise:
'''



RESULTS_THREAD_BODY = '''
Back on {created_time}, /u/{promiser_id} made a micropromise:

[{promise_title}]({original_post_link})

They got {n_pledges} pledges, from:\n\n
/u/{pledgerss}

How did they do?\n\n
'''


PROMISE_MESSAGE_BODY = '''
Hey! Your promise '{promise_title}' has expired.
Come join us in the results thread:
https://www.reddit.com/r/micropromise/comments/{results_thread_id}/

and write a comment starting with [KEPT] to tell us you succeeded.
Didn't succeed? Don't worry about it! We all have stuff going on, 
what's important is you're thinking on the right track.

Feel free to start a new promise thread and keep the dream alive!
'''


PLEDGE_MESSAGE_BODY = '''You kindly pledged to help {promiser_id} with their promise.
Come and contribute to the results thread here:
	https://www.reddit.com/r/micropromise/comments/{results_thread_id}/

And/or reply to this message to let us know how you did!
'''


WATCHER_MESSAGE_BODY = '''
You asked to watch {promiser_id} and their promise on /r/micropromise.
Check out the results thread here:
	https://www.reddit.com/r/micropromise/comments/{results_thread_id}/
'''