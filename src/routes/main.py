from fastapi import FastAPI
from dotenv import load_dotenv
from src.routes import base,data
import asyncio
import asyncio
from src.stores.llm.providers.LLMfactory import LLMProviderFactory
from src.stores.llm.providers.CoherProvider import Coher
from pymongo import AsyncMongoClient
from src.helpers.config import get_settings
app=FastAPI()

@app.on_event("startup")
async def start_up_db_client():
    settings=get_settings()
    app.mongo_connection=AsyncMongoClient(settings.MONGO_URL)
    app.db_client=app.mongo_connection[settings.MONGO_DATABASE]

    llm_provider_factory=LLMProviderFactory(settings)
    
    # generation client 
    app.generation_client=llm_provider_factory.create(provider=settings.GENERATION_BACK_END)
    app.generation_client.set_generation_model(model_id=settings.GENERATION_MODEL_ID)

    # embedding client 
    app.embedding_client=llm_provider_factory.create(provider=settings.EMBEDDING_BACK_END)
    app.embedding_client.set_embedding_model(model_id=settings.GENERATION_MODEL_ID,embeding_size=settings.EMBEDDING_MODEL_SIZE)




@app.on_event("shutdown")
async def shut_down_db_client():
    app.mongo_connection.close()


app.include_router(base.base_router)
app.include_router(data.data_router)