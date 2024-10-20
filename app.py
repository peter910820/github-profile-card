from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

from src.api import ApiGet

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    print("Current Working Directory: ", os.getcwd())
    return templates.TemplateResponse(
        request=request, name="index.html"
    )

@app.get("/api/{user}")
async def api(request: Request, user: str):
    api_get = ApiGet(user)
    api_get.get_data()
    api_get.draw_chart_pygal()
    return {"result": None}

@app.post("/search")
async def api(request: Request, user: str):
    pass