from src.controllers.Base_data_controllers import Base_controllers
from fastapi import UploadFile
from src.models.enums.response_enums import Responses
import os

class Category_cntroller(Base_controllers):
    def __init__(self):
        super().__init__()
    async def create_folder_for_each_category(self,category:str):
        project_dir_path=os.path.join(
            self.base_path,
            category
        )
        if not os.path.exists(project_dir_path):
            os.makedirs(project_dir_path)

        return project_dir_path
