from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import HTMLResponse
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "app/templates"))

# mount static files
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "app/static")),
    name="static"
)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )