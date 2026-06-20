import json
from typing import List
from src.models.db_schemes.chunks import Chunk
from fastapi import FastAPI,APIRouter,Depends, File, Form,UploadFile,Request
import os
from src.repository.chunk_model import Chunk_model
from fastapi.responses import JSONResponse
from pydantic import ValidationError 

from src.models.db_schemes.Autism_chat_bot_postgres.scheme.books import Books
from src.models.db_schemes.Autism_chat_bot_postgres.scheme.papers import Papers


from src.helpers.config import get_settings,Settings
from src.controllers.Datacontrollers import Datacontrollers
from src.models.enums.response_enums import Responses
from src.controllers.category_folder_creation_cntroller import Category_cntroller
import aiofiles
import logging
from src.repository.data_base_category_models import CategoryRepository
from src.routes.schemes.data import ProcssRequest
from src.controllers.process_file_controller import Process_controller
from src.models.category_collection_model import Category
from src.models.enums.response_enums import Responses

logger=logging.getLogger('uvicorn.error')
data_router=APIRouter(
    tags=["router for uploading apps"]
)
#جوا الداتا بيز 
#زمان كان لما يرفعلي كتيجوري اي دي كنت اعمله فولدر دلوقتي هعمله كوليكشن 
@data_router.post("/upload/{category_id}")
async def upload_data(request:Request,category_id:str,file:UploadFile,data:str=Form(...),app_settings:Settings=Depends(get_settings)):
    parsed = json.loads(data)
    category_repo=CategoryRepository(
          db_client=request.app.db_client,
          db_name="Autism_chat_bot"
    )
    

    category=Category(name=category_id)
    category_new=await category_repo. get_category_or_create(
          category=category
    )
    collection = request.app.db_client[category_id]

    result=Datacontrollers().validate_upload_file(file=file)
    if result:
            category_dir_path=await Category_cntroller().create_folder_for_each_category(category=category_id)
            file_path=os.path.join(
            category_dir_path,file.filename
            )
            async with aiofiles.open(file_path,"wb") as f:
                while chunk :=await file.read(app_settings.CHUNK_SIZE):
                    await f.write(chunk)
            parsed["file_name"] = file.filename
            parsed["file_path"] = file_path
            if category_id=="books":
                      book = Book(**parsed)
                      await collection.insert_one(book.dict())
            elif category_id=="papers":
                     paper=Paper(**parsed)
                     await collection.insert_one(paper.dict())
            return {
    "signal": Responses.FILE_TYPE_SUPPORTED,
    "message": Responses.FILE_UPLOADED_SUCCESSFULY

}

    else:
            return {"signal": Responses.FILE_TYPE_NOT_SUPPORTED}

    




@data_router.post("/file_process/{category_id}/chunks")
async def process_validation (request: Request,
                              category_id: str,
                              file: UploadFile= File(...),
                              chunk_size: int = Form(...),
                              over_lap: int = Form(...),

                              ):
    
      category_repo=CategoryRepository(
          db_client=request.app.db_client,
          db_name="Autism_chat_bot")
      category=Category(name=category_id)
      await category_repo.create_category_chunks_for_indexing(category=category)

      #file_category=process_request.file_category
      
      file_name = file.filename
      process_controller=Process_controller(category_id=category_id)

      file_content=process_controller.get_file_content(category_id=category_id,file_name=file_name)
      #if file_content==None:
           # return Responses.FILE_NOT_FOUNDED_IN_DATA_BASE.value
           #logger.error(Responses.FILE_NOT_FOUNDED_IN_DATA_BASE.value)
           #continue
           #  # دة في حالة البالك اني مديله مثلا ليست للكتب يعمل شانك
           #  احنا فاصلين اللوجيك كنا عاملين اند بوينت للبروسيس لفايل واحد
           #  وعاملين واحدة للبالك طبعا البالك هيبقا فيه ليست فلازم كونتنيو 
           # عشان تاخد الفايل الي وراه ومفروض برضو اننا مش هنديله الفايل 
           # هنسيرش في الكوليكشن الي تبعه موجود هناخده نعمل شانك

      file_chunks=process_controller.process_file_content(file_content=file_content,category_id=category_id,chunk_size=chunk_size,overlap_size=over_lap)

      if file_chunks is None or len(file_chunks) == 0:
            return JSONResponse(
                  status_code=400,
                  content={
                        "signal":Responses.FILE_PROCESSING_FAILED
                  }
            )
      

      else:
             
             file_chunks_records=[
                  Chunk(
                        document_id=category_id,
                        document_name=file_name,
                        chunk_index=i+1,
                        content=chunk.page_content.encode("utf-8", errors="ignore").decode("utf-8") ,
                         metadata=chunk.metadata )

                  
                  for i,chunk in enumerate(file_chunks)]
             
            
             chunk_model=Chunk_model(db_client=request.app.db_client,collection_name=f"{category_id}_chunks")
             number_of_records=await chunk_model.insert_many_chunks(chunks=file_chunks_records)
             
      return number_of_records






@data_router.post("/bulk_upload/{category_id}")
async def bulk_upload_data(
    request: Request,
    category_id: str,
    files: List[UploadFile],
    data: str = Form(...),
    app_settings: Settings = Depends(get_settings)
):
    parsed = json.loads(data)
    # convert to python dic 

    category_repo = CategoryRepository(
        db_client=request.app.db_client,
        db_name="Autism_chat_bot"
    )

    category = Category(name=category_id)
    category_new = await category_repo.get_category_or_create(category=category)
    collection = request.app.db_client[category_id]

    uploaded_files_info = []

    for i,file in enumerate(files):
        result = Datacontrollers().validate_upload_file(file=file)
        if not result:
            return {"signal": Responses.FILE_TYPE_NOT_SUPPORTED}

        category_dir_path = await Category_cntroller().create_folder_for_each_category(category=category_id)
        file_path = os.path.join(category_dir_path, file.filename)

        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.CHUNK_SIZE):
                await f.write(chunk)

        file_info = {
            "file_name": file.filename,
            "file_path": file_path
        }

        # Merge parsed data with file info
        current_parsed = parsed[i]
        parsed_with_file = {**current_parsed, **file_info}

        if category_id == "books":
            book = Book(**parsed_with_file)
            await collection.insert_one(book.dict())
        elif category_id == "papers":
            paper = Paper(**parsed_with_file)
            await collection.insert_one(paper.dict())

        uploaded_files_info.append(file_info)

    return {
        "signal": Responses.FILE_TYPE_SUPPORTED,
        "message": Responses.FILE_UPLOADED_SUCCESSFULY,
        "uploaded_files": uploaded_files_info
    }









            



    
    
    
  