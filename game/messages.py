from os import listdir, path
from pyyaml import loads
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

