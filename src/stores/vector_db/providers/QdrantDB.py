import uuid
from src.models.db_schemes.chunks import RetrivedOcument
from qdrant_client import models, QdrantClient
from src.stores.vector_db.vectordb_interface import VectorDBInterface
from src.stores.vector_db.vector_db_enums import DistanceMethodEnums
import logging
from typing import List

class QdrantDBProvider(VectorDBInterface):

    def __init__(self, db_path: str, distance_method: str, db_host: str = "localhost", db_port: int = 6333):
        self.client = None
        self.db_path = db_path
        self.db_host = db_host
        self.db_port = db_port

        if distance_method == DistanceMethodEnums.COSINE.value:
            self.distance_method = models.Distance.COSINE
        elif distance_method == DistanceMethodEnums.DOT.value:
            self.distance_method = models.Distance.DOT

        self.logger = logging.getLogger(__name__)

    def connect(self, use_cloud: bool = False, cloud_url: str = None, api_key: str = None):
        if use_cloud and cloud_url and api_key:
            self.client = QdrantClient(url=cloud_url, api_key=api_key)
        else:
            self.client = QdrantClient(host=self.db_host, port=self.db_port)

    def disconnect(self):
        self.client = None

    def is_collection_existed(self, collection_name: str) -> bool:
        return self.client.collection_exists(collection_name=collection_name)
    
    def list_all_collections(self) -> List:
        return self.client.get_collections()
    
    def get_collection_info(self, collection_name: str) -> dict:
        return self.client.get_collection(collection_name=collection_name)
    
    def delete_collection(self, collection_name: str):
        if self.is_collection_existed(collection_name):
            return self.client.delete_collection(collection_name=collection_name)
        
    def create_collection(self, collection_name: str, 
                                embedding_size: int,
                                do_reset: bool = False):
        if do_reset:
            _ = self.delete_collection(collection_name=collection_name)
        
        if not self.is_collection_existed(collection_name):
            _ = self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=embedding_size,
                    distance=self.distance_method
                )
            )

            return True
        
        return False
    
    def insert_one(self, collection_name: str, text: str, vector: list,
                         metadata: dict = None, 
                         document_name: str = None):
        
        if not self.is_collection_existed(collection_name):
            self.logger.error(f"Can not insert new record to non-existed collection: {collection_name}")
            return False
        
        try:
            _ = self.client.upload_records(
                collection_name=collection_name,
                records=[
                    models.Record(
                        vector=vector,
                        payload={
                            "text": text, "metadata": metadata,"document_name":document_name
                        }
                    )
                ]
            )
        except Exception as e:
            self.logger.error(f"Error while inserting batch: {e}")
            return False

        return True
    
    def insert_many(self, collection_name: str, texts: list, 
                          vectors: list, metadata: list = None, 
                          document_name: list = None, batch_size: int = 50):
        
        if metadata is None:
            metadata = [None] * len(texts)

        
        for i in range(0, len(texts), batch_size):
            batch_end = i + batch_size

            batch_texts = texts[i:batch_end]
            batch_vectors = vectors[i:batch_end]
            batch_metadata = metadata[i:batch_end]
            batch_document_name=document_name[i:batch_end]

            batch_records = [
                models.Record(
                            id=str(uuid.uuid4()),        # ← add this
                    vector=batch_vectors[x],
                    payload={
                        "text": batch_texts[x], "metadata": batch_metadata[x],"document_name":batch_document_name[x]
                    }
                )

                for x in range(len(batch_texts))
            ]

            try:
                _ = self.client.upload_records(
                    collection_name=collection_name,
                    records=batch_records,
                )
            except Exception as e:
                self.logger.error(f"Error while inserting batch: {e}")
                return False

        return True
        
    def search_by_vector(self, collection_name: str, vector: list, limit: int = 5):

        results= self.client.search(
            collection_name=collection_name,
            query_vector=vector,
            limit=limit
        )

        if not results or len(results)==0:
            return None
        
        return [
            RetrivedOcument(**{
                "score":result.score,
                "content":result.payload["text"]
            })
            for result in results
        ]
        

    

    