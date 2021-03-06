import io

import pandas
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="static")


@app.get("/")
def hello():
    return "Hello!"


@app.get("/main", response_class=HTMLResponse)
def main(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})


@app.get("/download-excel")
def download_excel():
    content = io.BytesIO()

    writer = pandas.ExcelWriter(path=content, engine="xlsxwriter")

    pandas.DataFrame(data={"a": [1, 2], "b": [3, 4]}).to_excel(
        writer, sheet_name="Sheet Name"
    )

    writer.save()
    content.seek(0)

    return StreamingResponse(content)
