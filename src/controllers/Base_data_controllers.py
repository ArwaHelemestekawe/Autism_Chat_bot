from src.helpers.config import Settings,get_settings
import os
class Base_controllers():
# الي كل شايفه
    def __init__(self):
        self.app=get_settings()
        # يكون في كلاس فيه كل سيتينجس ونقدر نورثه 
        self.base_path=r"/mnt/c/Users/arwah/Autism_Chat_bot/src/assets/data"
        self.data_base_dir =os.path.join(
            self.base_path,
            "vector_database"  # dir
        )


    def get_data_base_path(self,db_name):
            data_base_path=os.path.join(
                self.data_base_dir,
                db_name
            )

            if not os.path.exists(data_base_path):
                os.makedirs(data_base_path)

            return data_base_path













        