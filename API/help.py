import ujson

def save_data(data, name):
    f=open(name,"w") # opens a file for writing.
    f.write(ujson.dumps(data))
    f.close()

def load_data(name):
    f=open(name,"r")
    # print(f.read())
    data = ujson.load(f)
    # print("OLD DATA:", data)
    f.close()
    return data
