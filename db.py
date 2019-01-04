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


def insert_promise(row):
	c = db.cursor()
	c.execute('''
			INSERT INTO promises
			VALUES
			(?,?,?,?,?,?,?, 1, ?)
		''', 
		row
	)
	db.commit()
	c.close()


def insert_pledge(row):
	c.execute('''
			insert into pledges 
			values
			(?,?,?,?)
		''', 
		row
	)
	db.commit()
	c.close()


def insert_watcher(row):
	c = db.cursor()
	c.execute('''
		INSERT INTO watchers
		values
			(?,?,?)
	''', 
		row
	)
	db.commit()
	c.close()


def get_pledges():
	c = db.cursor()
	c.execute('''
		select comment_id from pledges
	''')
	pledges = [i[0] for i in c.fetchall()]
	return pledges


def get_finished_promises():
	c = db.cursor()
	c.execute('''
		select * from promises
		where live = 1
		and datetime(elapses_time,\'unixepoch\')<datetime(\'now\')
			
	''')
	finished_promises = c.fetchall()
	c.close()
	return finished_promises


def update_finished_promise(promise_id):
	c = db.cursor()
	c.execute(f'''
		update promises
		set live = 0 
		where id = '{promise_id}'
	''')
	db.commit()
	c.close()