from routers.auth import router as auth_api
from routers.user import router as user_api
from routers.blog import router as blog_api

routers = [
    auth_api,
    user_api,
    blog_api,
]
