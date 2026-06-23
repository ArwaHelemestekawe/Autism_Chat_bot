import json
import time
from src.repository.chunk_model import Chunk_model
from src.controllers.Base_data_controllers import Base_controllers
from src.models.db_schemes.books import Book
from src.models.db_schemes.papers import Paper
from src.models.db_schemes.chunks import Chunk 
from src.stores.vector_db.providers.QdrantDB import QdrantDBProvider
from src.stores.llm.llm_enum import Document_type
from typing import List
from src.models.enums.response_enums import Responses

class Nlp_controller(Base_controllers):
    def __init__(self,db_vectorclient,generation_model,embedding_model,templete_parser):
        super().__init__()

        self.vector_dbclient=db_vectorclient
        self.generation_model=generation_model
        self.embedding_model=embedding_model
        self.templete_parser=templete_parser

    def reset_vector_db_collection(self,category_id:str):
        collection_name=category_id
        return  self.vector_dbclient.delete_collection(collection_name=collection_name)
    
    def get_vector_collection_info(self,collection_id:str):
          # each category will have a collection cantains vectors

          collection_info=self.vector_dbclient.get_collection_info(collection_name=collection_id)
          return collection_info
    

    async def index_into_vector_db(self, collection_id, chunks, chunk_model:Chunk_model,do_rest=False):
        _ = self.vector_dbclient.create_collection(collection_name=collection_id, 
                                embedding_size=1024,
                                do_reset=do_rest)
        
        chunks=[c for c in chunks if not c.is_vectorized]


        text = [c.content for c in chunks]
        metadata = [c.metadata for c in chunks]
        document_name = [c.document_name for c in chunks]

        # embed in batches of 90 with delay to avoid rate limit
        vectors = []
        batch_size = 30
        for i in range(0, len(text), batch_size):
            batch = text[i:i + batch_size]
            batch_vectors = [
                self.embedding_model.embed_text(
                    text=t,
                    document_type=Document_type.DOCUMENT.value
                ) for t in batch
            ]
            vectors.extend(batch_vectors)
            if i + batch_size < len(text):
                time.sleep(61)  # wait 61 seconds before next batch

        _ = self.vector_dbclient.insert_many(
            collection_name=collection_id,
            texts=text,
            vectors=vectors,
            metadata=metadata,
            document_name=document_name
        )

        chunk_ids = [c.id for c in chunks] # نحتفظ بيهم عشان نعرف انهي الي حصله شانكينج تحديدا 
        await chunk_model.mark_chunks_as_vectorized(chunk_ids)


        return True
    

    def search_query(self,category_id:str,text:str,limit=5):
        collection_name=category_id
        vector_query=self.embedding_model.embed_text(text=text,document_type=Document_type.QUERY.value)

        if not vector_query or len(vector_query)==0:
            return Responses.QUERY_VECTOR_IS_NOT_FOUNDED.value
        
        else:
           retrived_document= self.vector_dbclient.search_by_vector(collection_name=category_id, vector=vector_query, limit=limit)

        return retrived_document
    
    def answer_rag_question(self,category_id:str,query:str,limit:int =5):
        retrived_documents= self.search_query(category_id=category_id,text=query)
        if not retrived_documents or len(retrived_documents)==0:
            return None 
        
        system_prompt=self.templete_parser.get("rag","system_prompt")

        

        documents_prompts="\n".join([         
                self.templete_parser.get(
                    "rag","document_prompt",{
                        "doc_num":idx+1,
                        "chunk_text":doc.content

                    }
                )
            
            
            for idx,doc in enumerate(retrived_documents)
                    ])
         
        footer_prompt=self.templete_parser.get("rag","footer_prompt",{
            "query":query
        })

        chat_history=[
            self.generation_model.construct_prompt(prompt_input=system_prompt,role=self.generation_model.enums.SYSTEM.value)
        ] #system message 

        full_prompt= "\n\n".join([documents_prompts,footer_prompt])     #footer &docs

        answer=self.generation_model.generate_text(prompt_input=full_prompt,chat_history=chat_history,max_output_tokens=500)

        return answer, full_prompt,chat_history,footer_prompt







         




    