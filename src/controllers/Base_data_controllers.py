from src.helpers.config import Settings,get_settings

class Base_controllers():
# الي كل شايفه
    def __init__(self):
        self.app=get_settings()
        # يكون في كلاس فيه كل سيتينجس ونقدر نورثه 
        self.base_path=r"/mnt/c/Users/arwah/Autism_Chat_bot/src/assets/data"
    