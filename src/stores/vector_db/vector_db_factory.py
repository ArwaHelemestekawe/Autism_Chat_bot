from src.stores.vector_db.providers.QdrantDB import QdrantDBProvider
from src.stores.vector_db.vector_db_enums import VectorDBEnums
from src.controllers.Base_data_controllers import Base_controllers

class VectorDBProviderFactory:
    def __init__(self, config):
        self.config = config
        self.base_controller = Base_controllers()

    def create(self, provider: str):
        if provider == VectorDBEnums.QDRANT.value:
            db_path = self.base_controller.get_data_base_path(db_name=self.config.VECTOR_DB_PATH)

            return QdrantDBProvider(
                db_path=db_path,
                distance_method=self.config.VECTOR_DB_DISTANCE_METHOD,
                db_host=self.config.QDRANT_HOST,
                db_port=self.config.QDRANT_PORT,
            )
                    
        return None