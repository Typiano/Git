from fastapi import FastAPI, Path
from typing_extensions import Annotated
import sys, help, uvicorn

print("Python version: " + sys.version)
app = FastAPI()


Startdaten = help.load_data("Daten.dat")
Temperatur = Startdaten["Temperatur"]
status = Startdaten["status"]
TempZusatznachricht = Startdaten["TempZusatznachricht"]
text = Startdaten["text"]

@app.get("/")
async def root():
    return "Hello to the server, if u want so see the Funktions, write /docs"

@app.get("/stat")
async def ret_status():
    return {"status" : status}

@app.get("/stat/{val}")
@app.post("/stat/{val}")
async def set_status(val: Annotated[int, Path(ge=1, le=6)]):
    global status, Startdaten
    status = val
    Startdaten["status"] = status
    help.save_data(Startdaten, "Daten.dat")
    return {"status": status, "message" : "status changed to " + str(status)}

@app.get("/tempstat")
async def ret_stat_Temp():
    global Temperatur, TempZusatznachricht
    if Temperatur <= 0:
        k = "kalt"
    elif Temperatur <= 18:
        k = "kuehl"
    elif Temperatur <= 33:
        k = "angenehm"
    elif Temperatur < 50:
        k = "heiss"
    else:
        k = "kochend"
    return {"Temperatur": Temperatur, "TempZusatz": TempZusatznachricht[k]}

@app.post("/tempstat/{temp}")
@app.get("/tempstat/{temp}")
async def set_stat_Temp(temp: Annotated[float, Path(ge=-50, le=100)]):
    global Temperatur, TempZusatznachricht, Startdaten
    Temperatur = temp
    Startdaten["Temperatur"] = Temperatur
    help.save_data(Startdaten, "Daten.dat")
    if temp <= 0:
        k = "kalt"
    elif temp <= 18:
        k = "kuehl"
    elif temp <= 33:
        k = "angenehm"
    elif temp < 50:
        k = "heiss"
    else:
        k = "kochend"
    return {"Temperatur": Temperatur, "TempZusatz": TempZusatznachricht[k]}


@app.get("/aenderstatustext{statusae}/{Ntext}")
@app.post("/aenderstatustext{statusae}/{Ntext}")
async def set_text_to_status(statusae: Annotated[int, Path(ge=1, le=6)], Ntext: str):
    global Startdaten
    Startdaten["text"][str(statusae)] =  Ntext
    help.save_data(Startdaten, "Daten.dat")
    return f"Dem Status {statusae} wurde der Text {Ntext} zugeordnet"

@app.get("/aenderWettertext{Wstatus}/{NWtext}") # =WetterStatus bzw NeuerWetterText
@app.post("/aenderWettertext{Wstatus}/{NWtext}")
async def set_Wtext_to_Wstatus(Wstatus: str, NWtext: str):
    global Startdaten
    Startdaten["TempZusatznachricht"][Wstatus] =  NWtext
    help.save_data(Startdaten, "Daten.dat")
    return f"Dem Wetter-Status {Wstatus} wurde der Text {NWtext} zugeordnet"

@app.get("/statustext")
async def get_status_text():
    global text, status
    return {"status": status, "text": text[str(status)]}

@app.get("/text/{nmbr}")
async def get_text(nmbr: Annotated[int, Path(ge=0, le=6)]):
    global status, text
    return {"status": nmbr, "text": text[str(nmbr)] }



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, log_level="info")