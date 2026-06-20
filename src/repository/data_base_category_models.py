import datetime
from sqlite3 import Cursor

from fastapi import UploadFile
from src.repository.data_base_base_model import  Data_base_Base_mode
from pymongo import MongoClient
from src.models.db_schemes.books import Book  
from src.models.db_schemes.chunks import Chunk
from src.models.category_collection_model import Category

class CategoryRepository(Data_base_Base_mode):
    def __init__(self, db_client: object, db_name: str):
        super().__init__(db_client=db_client)
        self.db = db_client

    
    '''
    async def create_category_chunks_for_indexing(self, category: Category):
        # هنا انا محتاجة اعمل انديكسينج علي مستوي الكوليكشن بتاعت الشانكس بس الي بتتعمل في فانكشن في البروسيس فايل 
        # مجرد الابلود هينادي  كرييت كاتيجوري في الكوليكشن العادية الي بتتحتفظ بس بالميتا داتا بتاعت الملفات
        # هنا انا بعمل كوليكشن مش شانكنج خالص 
        category_name=category.name
        chunks_collection_name = f"{category_name}_chunks"
        
        
        all_collections=await self.db_client.list_collection_names()
        if chunks_collection_name not in all_collections: # new collection
            self.collection = self.db[chunks_collection_name] 
            indexes=Chunk.get_index()
            for index in indexes:
                await self.collection.create_index(
                    index["key"],
                    name=index["name"],
                    unique=index["unique"]
                )

       
        return f"collection:{category_name} chunks is created"
        '''


    


    async def create_category(self, category: Category):
        # dynamically select collection
        category_name=category.name
        collection = self.db[category_name] 
       # result = await collection.insert_one(category.dict())
        #return result.inserted_id
        return f"collection:{category_name} is created"



    async def get_category_or_create(self, category:Category):
        
        await self.create_category(category=category)
        category_name=category.name
        collection = self.db[category_name]
        return f"Collection {category_name} is ready"
    

    async def add_documents(self,category:Category,file_name:str,file_path:str):
        collection=self.db_client[category.name]
        document = {
            "file_name": file_name,
            "file_path":file_path,
        }
       # result = await collection.insert_one(document)
        return document


    


        

    
    async def get_all_documents_in_specific_collection(self, page: int=1, page_size:int=10,collection_name: str = "books"):
        collection = self.db[collection_name]
    # count total number of documents
        total_documents = await collection.count_documents({})
        # calculate total number of pages
        total_pages = total_documents // page_size
        if total_documents % page_size > 0: # فيه دوكيمنتس  برة كابسيتي بتاعت اخر صفحة فهنزود صفحة 
            total_pages += 1

        cursor = collection.find().skip((page-1) * page_size).limit(page_size)
        documents=[]
        async for document in cursor:
            documents.append(
            Book.model_validate(document)
            )

        return documents, total_pages

        
        
        
       
