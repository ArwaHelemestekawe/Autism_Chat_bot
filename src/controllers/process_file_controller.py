from src.controllers.Base_data_controllers import Base_controllers
import os 
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader
from src.models.enums.enum_file_processing import File_processing_extension
from src.models.enums.response_enums import Responses

from langchain_community.document_loaders import UnstructuredEPubLoader
from src.controllers.Base_data_controllers import Base_controllers
from langchain_text_splitters import RecursiveCharacterTextSplitter
class Process_controller(Base_controllers):
    def __init__(self,category_id:str):
        super().__init__()

        self.category_id=category_id

    def validate_file_extension(self,file_name:str):
        return os.path.splitext(file_name)[-1]
    
    
    def get_file_loader(self,category_id:str,file_name:str):
        file_extenstion=self.validate_file_extension(file_name=file_name)
        base_path=Base_controllers().base_path
        file_path=os.path.join(
            base_path,category_id,file_name
        )
       # if os.file_path==None:
       # return Responses.FILE_NOT_FOUNDED_IN_DATA_BASE.value
        if file_extenstion== File_processing_extension.TXT.value:
            return TextLoader(file_path=file_path, encoding="utf-8", autodetect_encoding=True)
        elif file_extenstion== File_processing_extension.PDF.value:
            return PyMuPDFLoader(file_path=file_path)
        elif file_extenstion== File_processing_extension.epup.value:
            return UnstructuredEPubLoader(file_path=file_path)
        
    
    def get_file_content(self,category_id:str,file_name:str):
       loader=self.get_file_loader(category_id=category_id,file_name=file_name) 
       if loader:
        return loader.load()
       #else:
           #n return Responses.FILE_NOT_FOUNDED_IN_DATA_BASE.value
    # اللودر بيرجع ليست فيها ميتا داتا وفيها كل الصفح
    
    def process_file_content(self,file_content:list,category_id:str,
                             chunk_size:int=100,overlap_size:int=20):
        text_splitter=RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap_size,
            length_function=len
        )

        file_content_texts=[rec.page_content for rec in file_content ]

        file_content_meta_data=[rec.metadata for rec in file_content ]

        chunks=text_splitter.create_documents(
            file_content_texts,
            metadatas=file_content_meta_data
        )

        return chunks




        

    


    


        