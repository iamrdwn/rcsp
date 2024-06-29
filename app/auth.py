
from authlib.integrations.starlette_client import OAuth, OAuthError
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, APIRouter, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi.templating import Jinja2Templates
from starlette.config import Config
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app import schemas

# Load environment variables
load_dotenv()

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(
    # prefix="/auth",
    tags=["auth"]
)

config = Config('.env')

GOOGLE_CLIENT_ID = config('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = config('GOOGLE_CLIENT_SECRET')

oauth = OAuth(config)

oauth.register(name='google', client_id=GOOGLE_CLIENT_ID, client_secret=GOOGLE_CLIENT_SECRET,
    # authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None, authorize_state='secret-key',
    # access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None, server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    refresh_token_url=None, redirect_uri='http://localhost:8000/auth/callback',
    client_kwargs={'scope': 'openid profile email'}, )

oauth2_scheme = OAuth2AuthorizationCodeBearer(tokenUrl='/auth/login',
                                              authorizationUrl='https://accounts.google.com/o/oauth2/auth')


def get_current_user(request: Request):
    # Retrieve the current user based on the token
    # In this example, we assume the user is stored in the session

    user = request.session.get('user')

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated", )

    return schemas.User(**user)


@router.get('/auth/login')
async def login(request: Request):
    redirect_uri = request.url_for('auth_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get('/login')
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.route('/auth/callback')
async def auth_callback(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        raise HTTPException(status_code=401, detail=f'Authentication failed.{error.error}')
    user = token.get('userinfo')
    user['id'] = user.pop('sub')
    if user:
        request.session['user'] = dict(user)
    return RedirectResponse(url='/')


@router.get('/auth/logout')
async def logout(request: Request):
    # Handle logout logic, e.g., clearing session cookies or tokens
    request.session.pop('user', None)
    return templates.TemplateResponse("login.html", {"request": request})


@router.get('/users/me', response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(get_current_user)):
    return current_user

def get_current_user_dep(request: Request):
    return get_current_user(request)
