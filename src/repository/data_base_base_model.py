from src.helpers.config import get_settings
class Data_base_Base_mode:
    def __init__(self,db_client:object):
        self.db_client=db_client
        self.app_settings=get_settings()