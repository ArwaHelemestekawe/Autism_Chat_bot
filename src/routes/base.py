from fastapi import FastAPI,APIRouter,Depends
import os 
from src.helpers.config import get_settings,Settings

base_router=APIRouter(
    tags=["welcome response to ensure that chatbot is working "]
)

@base_router.get("/welcome")
async def welcome(app_settings:Settings=Depends(get_settings)):
    #app_settings= get_settings()
    # if getsettings is not existed or there is an error so welcome function will collapse so we need to acknowledge that there is a dependancy
    app_name=app_settings.APP_NAME
    app_version=app_settings.APP_VERSION

    return {
    "message":"welcome to ألفة chat bot:",
    "app_name":app_name,
    "app_version":app_version
}
