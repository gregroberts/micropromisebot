import sqlite3

db = sqlite3.connect('micropromise.db')

def create_schema():
	c = db.cursor()
	c.execute('''
		CREATE TABLE IF NOT EXISTS
			promises 
			(
				id text,
				title text,
				user_id text,
				created_time int,
				timeframe text,
				elapses_time int,
				bot_comment_id text,
				live int default 1,
				user_name text
			)
	''')
	c.execute('''
		CREATE TABLE IF NOT EXISTS pledges
		(
			promise_id text,
			comment_id text,
			user_name text,
			user_id text
		)
	''')
	c.execute('''
		CREATE TABLE IF NOT EXISTS watchers
		(
			promise_id text,
			user_name text,
			user_id text
		)
	''')
	db.commit()
	c.close()


def get_existent_promise_ids():
	print('getting existing promises')
	c = db.cursor()
	c.execute('SELECT id from promises')
	data = c.fetchall()
	c.close()
	return data


def get_promise(id):
	c = db.cursor()
	print(id)
	c.execute(f'''
		select * from promises 
		where id = '{id}'
		'''
	)
	data = c.fetchone()
	print(data)
	return data


def get_promise_pledges(promise_id):
	c = db.cursor()
	c.execute(f'''
		select * from pledges
		where promise_id = '{promise_id}'
	''')
	pledgers = c.fetchall()
	c.close()
	return pledgers


def get_promise_watchers(promise_id):
	c = db.cursor()
	c.execute(f'''
		select * from watchers
		where promise_id = '{promise_id}'
	''')
	watchers = c.fetchall()
	c.close()
	return watchers