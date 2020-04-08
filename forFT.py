'''
Plan

1. import json file

2. remove size attribute

3. remove item

4. price to int
'''


import json
import re


fp = json.load(open("out/crafting.json"))
k = 0
def p(s:str) -> int:
    try:
        return int(re.sub(r"[,()A-z]", "", s).strip())
    except:
        return 0
def a(i:dict) -> dict:
    global k
    o = {
        "id":f"i{str(k).zfill(4)}",
        "name":i["Recipe Name"],
        "materials": i["Materials Needed"],
        "obtained": i["Obtained From"],
        "price": p(i["Sell Price"])
    }
    k += 1
    return o

def main():
    return list(map(a,fp))


if __name__ == "__main__":
    json.dump(main(),open("out/FT/items.json", "w"))