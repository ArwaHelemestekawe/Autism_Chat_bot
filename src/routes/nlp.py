from fastapi import FastAPI,APIRouter,status,Request
from fastapi.responses import JSONResponse
from src.repository.data_base_category_models import CategoryRepository
from src.routes.schemes.nlp import PushRequest,SearchRequest
from src.models.category_collection_model import Category
import logging
from src.stores.llm.templete.temp_parser import TemplateParser
from src.controllers.nlp_controller import Nlp_controller
from src.repository.chunk_model import Chunk_model
from src.models.enums.response_enums import Responses
logger=logging.getLogger("uvicorn.error")

nlp_router=APIRouter(
    prefix="/nlp",
    tags=["vector embedding routes"]
)

@nlp_router.post("/index/push/{category_id}")
async def index_category(request:Request,category_id:str,push_request:PushRequest):
    category_repo=CategoryRepository(
          db_client=request.app.db_client,
          db_name="Autism_chat_bot"
    )

    chunk_model=  Chunk_model(db_client=request.app.db_client,collection_name=category_id)


    category=Category(name=category_id)
    category_new=await category_repo.get_category_or_create(
          category=category
    )

    if not category_new:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=(Responses.CATEGORY_NOT_FOUND.value)
        )
    
    nlp_controller=Nlp_controller(db_vectorclient=request.app.vector_db_client,
                                  generation_model=request.app.generation_client,
                            embedding_model=request.app.embedding_client,
                            templete_parser=request.app.temp_parser
                            )
    
    has_record=True
    page_number=1
    all_chunks=[]
    while has_record:
        chunks=await chunk_model.get_all_chunk_of_specific_category(category_id=category_id,page_num=page_number)
        if len(chunks):
            page_number+=1
            all_chunks.extend(chunks)

        if len(chunks)==0:
            has_record=False
            break
    is_inserted =await nlp_controller.index_into_vector_db(
        collection_id=category_id,
        chunks=all_chunks
        ,do_rest=push_request.do_reset,
        chunk_model=chunk_model)
    if not is_inserted:
        return Responses.CHUNK_VICTORIZED_failed
    else:
        return Responses.CHUNK_VICTORIZED_CORRECTLY
        
    


@nlp_router.get("/get_info/{category_id}")
async def get_info(request:Request,category_id:str):
    category_repo=CategoryRepository(
          db_client=request.app.db_client,
          db_name="Autism_chat_bot"
    )
    category=Category(name=category_id)
    category_new=await category_repo.get_category_or_create(
          category=category
    )

    nlp_controller=Nlp_controller(db_vectorclient=request.app.vector_db_client,
                                  generation_model=request.app.generation_client,
                            embedding_model=request.app.embedding_client,
                            templete_parser=request.app.temp_parser)


    collection_info=nlp_controller.get_vector_collection_info(collection_id=category_id)
    return  collection_info




@nlp_router.post("/search/{category_id}")
async def search(request:Request,category_id:str,search_request:SearchRequest):
    category_repo=CategoryRepository(
          db_client=request.app.db_client,
          db_name="Autism_chat_bot",

          
    )
    category=Category(name=category_id)
    category_new=await category_repo.get_category_or_create(
          category=category
    )

    nlp_controller=Nlp_controller(db_vectorclient=request.app.vector_db_client,
                                  generation_model=request.app.generation_client,
                            embedding_model=request.app.embedding_client,
                            templete_parser=request.app.temp_parser)


    results=nlp_controller.search_query(category_id=category_id,text=search_request.text,limit=search_request.limit)
    if not results:
        return Responses.SEARCH_QUERY_Fail.value
    else:
        return JSONResponse(
            content={
            "text":[result.dict() for result in results],
            "signal":Responses.SEARCH_QUERY_SUCCESS.value

        })
    

@nlp_router.post("/answer/{category_id}")
async def search(request:Request,category_id:str,search_request:SearchRequest):
    category_repo=CategoryRepository(
          db_client=request.app.db_client,
          db_name="Autism_chat_bot"
    )
    category=Category(name=category_id)
    category_new=await category_repo.get_category_or_create(
          category=category
    )

    nlp_controller=Nlp_controller(db_vectorclient=request.app.vector_db_client,
                                  generation_model=request.app.generation_client,
                            embedding_model=request.app.embedding_client,
                            templete_parser=request.app.temp_parser)
    
    answer, full_prompt,chat_history,footer_prompt=nlp_controller.answer_rag_question(category_id=category_id,query=search_request.text,limit=search_request.limit)

    if not answer:
        return JSONResponse(
            content={
                "signal":Responses.ANSWER_RAG_FAILED.value
            }
        )
    
    return   JSONResponse(
            content={
                #"signal":Responses.ANSWER_RAG_success.value,
                "content":answer,
                #"query": footer_prompt
            }
        )
    
