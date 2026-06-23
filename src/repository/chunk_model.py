from src.helpers.config import get_settings
from src.models.db_schemes.chunks import Chunk
from src.repository.data_base_base_model import Data_base_Base_mode
from bson.objectid import ObjectId
from pymongo import InsertOne
from bson import ObjectId
from src.models.enums.response_enums import Responses
class Chunk_model(Data_base_Base_mode):
    def __init__(self,db_client:object,collection_name:str):
        super().__init__(db_client=db_client)
        self.collection=self.db_client[collection_name]
    

    async def create_chunk(self,chunk:Chunk):
        result= await self.collection.insert_one(chunk.dict())
        chunk._id=result.inserted_id
        return chunk 
    
    async def get_chunk(self,book_name:str,chunk_id:str):
        result=await self.collection.find_one({
            "_id":ObjectId(chunk_id)
        })
        if result ==None:
            return Responses.CHUNK_NOT_FOUNDED.value
        
        else :
         return Chunk(**result)
        

    async def insert_many_chunks(self, chunks: list, batch_size: int=100):
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i+batch_size]

            operations = [
                InsertOne(chunk.dict())
                for chunk in batch
            ]

            await self.collection.bulk_write(operations)

        return len(chunks)
    

    async def get_all_chunk_of_specific_category(self,category_id:str,page_num:int=1,page_size:int=50):
        result=await self.collection.find({
            
        }).skip((page_num-1)*page_size).limit(page_size).to_list(length=None)

        return[
            Chunk(**rec)
            for rec in result
        ]
    

    async def mark_chunks_as_vectorized(self, chunk_ids: list):
        object_ids = [ObjectId(cid) for cid in chunk_ids]
        await self.collection.update_many(
            {"_id": {"$in": object_ids}},
            {"$set": {"is_vectorized": True}}
        )







