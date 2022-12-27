import json

def remplace_json(result,path):
    with open(path, "w", encoding="utf-8") as f:
        f.seek(0)
        f.write(json.dumps(result))
    return result

def read_json(path):
    with open(path,"r+",encoding="utf-8") as file:
        result= json.loads(file.read())
    return result

def include_json(path,dic):
    with open(path,"r+",encoding="utf-8") as file:
        results= json.loads(file.read())
        results.append(dic)
        file.seek(0)
        file.write(json.dumps(results))
    return results