import os

from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.api import ApiGet

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/chart", StaticFiles(directory="chart"), name="chart")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    print("Current Working Directory: ", os.getcwd())
    return templates.TemplateResponse(
        request=request, name="index.html"
    )


@app.get("/api/{user}")
async def api(request: Request, user: str):
    if user.strip() == "":
        return {"ERROR": "Username cannot be blank"}
    api_get = ApiGet(user)
    if api_get.get_data() is not None:
        return {"ERROR": "username not found"}
    api_get.draw_chart_pygal()
    return FileResponse(f"./chart/{user}_profile.svg")


@app.post("/search")
async def search(request: Request, user: str = Form(...)):
    if user.strip() == "":
        return {"ERROR": "Username cannot be blank"}
    api_get = ApiGet(user)
    if api_get.get_data() is not None:
        return {"ERROR": "username not found"}
    api_get.draw_chart_pygal()
    return FileResponse(f"./chart/{user}_profile.svg")
