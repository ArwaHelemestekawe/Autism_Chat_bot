from src.helpers.config import Settings,get_settings
from src.controllers.Base_data_controllers import Base_controllers
from fastapi import FastAPI,UploadFile


class Datacontrollers(Base_controllers):
    def __init__(self):
        super().__init__()

    

    def validate_upload_file(self,file:UploadFile):

        if file.content_type not in self.app.FILE_ALLOWED_EXTENSION:
            #print("not supported type only pdfs and text files")
            return False
        
        #print("type is valid")
        return True
    

        