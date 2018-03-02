import json

class User(object):
    def __init__(self, name):
        self.name = name
        self.uuu = "aaaa"


class UserEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, User):
            return obj.name
        return json.JSONEncoder.default(self, obj)

ss = User('orangle')

json_2 = {'user': ss}
xx = json.dumps(json_2, cls=UserEncoder)
ss = json.loads(xx,)
print ss['user'].name