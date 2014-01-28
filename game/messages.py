from os import listdir, path

import yaml

messages = []

def load_messages():
    for filename in listdir("game/data"):
        with open(path.join("game/data", filename)) as fp:
            messages.append( yaml.load(fp.read()) )

def mission_number(subject):
    for m in messages:
        if( m.get('subreply') == subject ):
            return m['id']
    return -1

def get_mission(mid):
    for m in messages:
        if m['id'] == mid:
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
