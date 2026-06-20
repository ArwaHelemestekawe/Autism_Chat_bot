from fastapi import FastAPI
from dotenv import load_dotenv
from src.routes import base,data,nlp
import asyncio
from src.stores.llm.templete.temp_parser import TemplateParser
from src.stores.vector_db.vector_db_factory import VectorDBProviderFactory
from src.stores.llm.LLMfactory import LLMProviderFactory
from src.stores.llm.providers.CoherProvider import Cohere
#from pymongo import AsyncMongoClient
from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession
from sqlalchemy.orm import sessionmaker
from src.helpers.config import get_settings
app=FastAPI()

@app.on_event("startup")
async def start_up_db_client():
    settings=get_settings()

    postgres_connection=f"postgressql+asyncpg://{settings.POSTGRES_USERNAME}:{settings.POSTGRES_PASSWORD}@localhost:5432/{settings.POSTGRESS_MAIN_DATA_BASE}"
    app.db_engine=create_async_engine(postgres_connection)
    app.db_client=sessionmaker(app.db_engine,
                               class_=AsyncSession,
                               expire_on_commit=False
                               )
    
    #app.mongo_connection=AsyncMongoClient(settings.MONGO_URL)
    #app.db_client=app.mongo_connection[settings.MONGO_DATABASE]

    llm_provider_factory=LLMProviderFactory(settings)
    vector_db_factory=VectorDBProviderFactory(settings)
    # generation client 
    app.generation_client=llm_provider_factory.create(provider=settings.GENERATION_BACK_END)
    app.generation_client.set_generation_model(model_id=settings.GENERATION_MODEL_ID)

    # embedding client 
    app.embedding_client=llm_provider_factory.create(provider=settings.EMBEDDING_BACK_END)
    app.embedding_client.set_embedding_model(model_id=settings.EMBEDDING_MODEL_ID,embeding_size=settings.EMBEDDING_MODEL_SIZE)
    
    # vactor data base client

    app.vector_db_client=vector_db_factory.create(settings.VECTOR_DB_BACKEND)
    app.vector_db_client.connect()

    #temp parser

    app.temp_parser=TemplateParser(settings.LANGUAGE)



@app.on_event("shutdown")
async def shut_down_db_client():
   app.db_engine.dispose()
   #await app.mongo_connection.close()
   app.vector_db_client.disconnect()


app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)

