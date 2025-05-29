from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from loguru import logger

from src.api import ApiGet

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/chart", StaticFiles(directory="chart"), name="chart")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )


@app.get("/api/{user}")
async def api(_: Request, user: str):
    return handle_generate_chart(user)


@app.post("/search")
async def search(_: Request, user: str = Form(...)):
    return handle_generate_chart(user)


def handle_generate_chart(user: str):  # utils
    if user.strip() == "":
        return {"ERROR": "Username cannot be blank"}
    try:
        api = ApiGet(user)
        api.generate_chart()
    except Exception as e:
        logger.error(e)
        return {"ERROR": "username not found"}
    return FileResponse(f"./chart/{user}_profile.svg")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=3010, reload=True)
