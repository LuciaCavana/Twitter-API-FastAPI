import json

from fastapi import HTTPException, status

def remplace_json(path,result):

        with open(path, "w", encoding="utf-8") as f:
            f.seek(0)
            f.write(json.dumps(result))
        return True
    

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

def update_json(path, dictionary, results,id):
    for user in results:
        if user["user_id"] == id:
            results[results.index(user)] = dictionary
            remplace_json(path,results)
            return dictionary,True
    else:
        dic = {}
        return dic,False


def return_entidad_expesifiqued(path, id, campo):
    results = read_json(path)

    for item in results:
        if item[campo] == id:
            return item
    