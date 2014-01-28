from os import listdir, path
from yaml import loads

messages = []

def load_messages():
    for filename in listdir("game/data"):
        with open(path.join("game/data", filename)) as fp:
            messages.append( loads(fp.read()) )

def mission_number(subject):
    for m in messages:
        if( m['subreply'] == subject ):
            return m['id']
    return -1

def get_mission(mid):
    for m in messages:
        if m['mid'] == mid:
            return m
    return None

def next_mission(mid):
    return get_mission(mid)['next_id']

def load_response(mission_id, success):
    """Passed next mission_id on success, last on failure."""
    if success:
        return get_mission(mission_id)['brief']
    else:
        return get_mission(mission_id)['reply_failed']
