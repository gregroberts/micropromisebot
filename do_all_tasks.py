from check_kept_promises import check_promise_keepers
from finish_promises import finish_all_promises
from handle_pledgers_watchers import handle_all_pledges, handle_all_watchers
from handle_promises import handle_all_promises
from handle_results_threads import handle_all_results_threads
from manage_flair import set_users_flair
from manage_post_flair import mark_all

def do_all():
	print('check_promise_keepers')
	check_promise_keepers()
	print('finish_all_promises')
	finish_all_promises()
	print('handle_all_pledges')
	handle_all_pledges()
	print('handle_all_watchers')
	handle_all_watchers()
	print('handle_all_promises')
	handle_all_promises()
	print('handle_all_results_threads')
	handle_all_results_threads()
	print('set_users_flair')
	set_users_flair()
	print('manage post flair')
	mark_all()



if __name__ == '__main__':
	do_all()