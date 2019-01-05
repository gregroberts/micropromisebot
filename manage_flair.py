from collections import defaultdict
from db import db
from reddit import *

def get_promises_scores():
    c = db.cursor()
    c.execute('''
    select
        user_name, 
        coalesce(sum(kept),0),
        count(distinct p.id)
    from promises p
    left join kept_promises k
    on p.id=k.id
    where live = 0
        group by user_name
    order by count(*) desc
    ''')
    scores = c.fetchall()
    c.close()
    return scores


def get_pledge_scores():
    c = db.cursor()
    c.execute('''
    select
        user_name, 
        coalesce(sum(kept),0),
        count(distinct promise_id)
    from pledges p
    left join kept_pledges k
    on p.comment_id=k.id
    where promise_id in (select id from promises where live = 0)
        group by user_name
    order by count(*) desc
    ''')
    scores = c.fetchall()
    c.close()
    return scores


def get_watch_scores():
    c = db.cursor()
    c.execute('''
    select
        user_name, count(distinct promise_id)
    from watchers
        group by user_name
    order by count(promise_id) desc
    ''')
    scores = c.fetchall()
    return scores


def get_users_scores():
    promise_scores = {
        i[0]:i[1:]
        for i in get_promises_scores()
    }
    pledge_scores =  {
        i[0]:i[1:]
        for i in get_pledge_scores()
    }
    watch_scores =  {
        i[0]:i[1]
        for i in get_watch_scores()
    }
    scores = defaultdict(lambda :{
        'promises_made':0,
        'promises_kept':0,
        'pledges_made':0,
        'pledges_kept':0,
        'promises_watched':0
    })
    for i, j in promise_scores.items():
        scores[i]['promises_made'] += j[1]
        scores[i]['promises_kept'] += j[0]
    for i, j in pledge_scores.items():
        scores[i]['pledges_made'] += j[1]
        scores[i]['pledges_kept'] += j[0] 
    for i, j in watch_scores.items():
        scores[i]['promises_watched'] += j  
    return scores

def get_badge(score):
    total_score = score['promises_made'] \
                + score['pledges_made'] \
                + score['promises_watched']
    quant_badge = ''
    if total_score <= 1:
        quant_badge += 'FRESH FACED'
    elif total_score <= 3:
        quant_badge += 'JOURNEYMAN'
    elif total_score <= 6:
        quant_badge += 'GENEROUS'
    else:
        quant_badge += 'PROLIFIC'
    qual_badge = ''
    if score['promises_made'] == 0:
        if score['pledges_made'] > 0:
            qual_badge +='LOYAL PLEDGE'
        else:
            qual_badge += 'CHEERLEADER'
    else:
        kept_perc = score['promises_kept'] / float(score['promises_made'])
        if kept_perc<=0.5:
            qual_badge += 'STARGAZER'
        elif kept_perc<1:
            qual_badge += 'ON A ROLL'
        elif kept_perc==1.0:
            qual_badge +='PERFECT BEING'
    badge = f'{quant_badge}, {qual_badge}'
    return badge


def build_flair(score):
    badge = get_badge(score)
    score['badge'] = badge
    score['promise_score'] = '{promises_kept}/{promises_made}'.format(**score)
    score['pledge_score'] = '{pledges_kept}/{pledges_made}'.format(**score)
    score['watched'] = '{promises_watched}'.format(**score)
    flair = '{badge}|{promise_score}|{pledge_score}|{watched}'.format(**score)
    return flair

def get_users_flair():
    scores = get_users_scores()
    flairs = {
        user: build_flair(score)
        for user, score in scores.items()
    }    
    return flairs

def set_users_flair():
    rt = get_reddit()
    mp = rt.subreddit('micropromise').flair
    for user, flair in get_users_flair().items():
        print(user,'-',flair)
        mp.set(user, flair)


if __name__ == '__main__':
    set_users_flair()
