from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from utils import get_id, get_data
import uvicorn


app = FastAPI()

templates = Jinja2Templates(directory="templates/")


@app.get("/", response_class=HTMLResponse)
def start_page(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})


@app.post("/", response_class=HTMLResponse)
def calculate(request: Request, url: str = Form("")):
    id_ = None
    try:
        id_ = get_id(url)
    except:
        final_text = "Invalid Playlist Link\n"
    if not id_:
        return templates.TemplateResponse(
            "index.html", context={"request": request, "final_text": final_text}
        )

    final_text = get_data(id_)
    return templates.TemplateResponse(
        "index.html", context={"request": request, "final_text": final_text}
    )


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)