from typing import List
from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from fastapi import WebSocket, WebSocketDisconnect

from .auth import router as oauth_router
from .routers import children, donors, donations
from .utils import ws_manager

templates = Jinja2Templates(directory="app/templates")

async def not_found_error(request: Request, exc: HTTPException):
    return templates.TemplateResponse('404.html', {'request': request}, status_code=404)

async def internal_error(request: Request, exc: HTTPException):
    return templates.TemplateResponse('500.html', {'request': request}, status_code=500)


exception_handlers = {
    404: not_found_error,
    500: internal_error
}

app = FastAPI(
    exception_handlers=exception_handlers
)
app.include_router(children.router)
app.include_router(donors.router)
app.include_router(donations.router)
app.add_middleware(SessionMiddleware, secret_key="secret-key")

app.include_router(oauth_router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

nav_routes = [
    {"name": "Home", "path": "/"}

]

templates.env.globals['nav_routes'] = nav_routes


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await ws_manager.broadcast(f"Client says: {data}")
            print(data)
            await ws_manager.send_personal_message(data, websocket)
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
        await ws_manager.broadcast("A client disconnected")


@app.get("/")
def read_root(request: Request):
    user = request.session.get('user')
    return templates.TemplateResponse("index.html", {"request": request, "title": 'Remote Child Sponsorship Program - CHINAR Kashmir' , 'nav_routes': nav_routes})

@app.get("/test_ws")
async def test_ws(request: Request):
    return templates.TemplateResponse("websocket.html", {"request": request})
