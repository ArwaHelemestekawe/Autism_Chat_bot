from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME:str
    APP_VERSION:str
    FILE_ALLOWED_EXTENSION:list
    CHUNK_SIZE:int
    MONGO_URL:str
    MONGO_DATABASE:str
    GENERATION_BACK_END:str
    EMBEDDING_BACK_END:str

    OPENAI_API_KEY:str
    OPEN_API_URL:str
    COHERE_API_KEY:str

    GENERATION_MODEL_ID:str
    EMBEDDING_MODEL_ID:str
    EMBEDDING_MODEL_SIZE:int


    INPUT_DEFAULT_MAX_CHARACTERS:int
    GENERATION_DEFAULT_MAX_CHARACTERS:int
    GENERATION_DEFAULT_MAX_TOKENS:int
    TEMPRETURE:float



    VECTOR_DB_BACKEND:str
    VECTOR_DB_PATH:str
    VECTOR_DB_DISTANCE_METHOD:str
    QDRANT_HOST: str 
    QDRANT_PORT: int 


    DEFAULT_LANGUAGE:str
    LANGUAGE:str



    class Config:
        env_file="src/.env"


def get_settings():
    return Settings()
