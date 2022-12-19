import json

def tuple_to_dict(tup, columns):
    resp = {}
    for i in range(len(tup)):
        resp[list(columns.keys())[i]] = tup[i]
    
    for k, v in columns.items():
        if v == list:
            resp[k] = json.loads(resp[k])

        elif v == dict:
            resp[k] = json.loads(resp[k])

        elif v == int:
            resp[k] = int(resp[k])

        elif v == bool:
            resp[k] = True if resp[k] == 'True' else False

        elif v == float:
            resp[k] = float(resp[k])

    return resp