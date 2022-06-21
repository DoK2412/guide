from fastapi import FastAPI
from .api import router
from .realizationUser import routerUsers


app = FastAPI()
app.include_router(router)
app.include_router(routerUsers)

