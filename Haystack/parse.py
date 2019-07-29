import json
result = {}
txt = ""
with open("quotes.json") as f:
  data = f.readlines()
  for ele in data:
    obj = json.loads(ele)
    id = int(obj["_id"])
    result[id] = obj["_source"]["quote"]
  for i in sorted(result.keys()):
    print(i)
    txt = txt + result[i] + "\n"
with open("result.md", "w") as f1:
  f1.write(txt)
#print(result)

