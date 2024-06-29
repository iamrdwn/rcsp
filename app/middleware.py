# app/middleware.py
from urllib.parse import urlencode

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.templating import Jinja2Templates
from starlette.responses import Response, RedirectResponse

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        if request.url.path not in ["/login", "/auth/"]:  # Exclude the login and static paths
            user = request.session.get("user")
            if not user:
                query_params = urlencode({"next": str(request.url)})
                login_url = f"/login?{query_params}"
                return RedirectResponse(url=login_url)
        response = await call_next(request)
        return response
