from fastapi import FastAPI, Path
from typing_extensions import Annotated
import sys
print("Python version: " + sys.version)

app = FastAPI()

status = 0
text = [ 
        "Nothing",
        "Hallo",
        "Foo",
        "Bar",
        "This tutorial shows you how to use FastAPI with most of its features, step by step. Each section gradually builds on the previous ones, but it's structured to separate topics, so that you can go directly to any specific one to solve your specific API needs. It is also built to work as a future reference. So you can come back and see exactly what you need.",
        "Hier könnte Ihre werbung stehen",
        "1337"
        ]


@app.get("/")
async def root():
    return {"message": "Hello World!!!"}

@app.get("/stat")
async def ret_status():
    return {"status" : status}

#@app.post("/stat/")
@app.get("/stat/{val}")
@app.post("/stat/{val}")
async def set_status(val: Annotated[int, Path(ge=0, le=6)]):
    global status
    status = val
    return {"status": status, "message" : "status changed to " + str(status)}

@app.get("/statustext")
async def get_status_text():
    global text, status
    return {"status": status, "message" : "Text for status " + str(status), "text": text[status] }

@app.get("/text/{nmbr}")
async def get_text(nmbr: Annotated[int, Path(ge=0, le=6)]):
    global status
    return {"status": status, "message" : "Text for status " + str(status), "text": text[nmbr] }



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")