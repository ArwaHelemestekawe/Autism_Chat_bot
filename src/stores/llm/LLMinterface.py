from abc import ABC,abstractmethod

class LLMInterface(ABC):
    @abstractmethod  # obligation to use this function otherwise will provide an error 
    def set_generation_model(self,model_id:str):
        pass

    @abstractmethod  # obligation to use this function otherwise will provide an error 
    def set_embedding_model(self,model_id:str,embeding_size:int):
        pass

    @abstractmethod  # obligation to use this function otherwise will provide an error 
    def generate_text(self,prompt_input:str,chat_history:list=[],max_output_tokens:int=None,tempreture:float=0.4):
        pass

    @abstractmethod  # obligation to use this function otherwise will provide an error 
    def embed_text(self,text:str,document_type=None):
        # big document or just a quary from user 
        pass

    @abstractmethod  # obligation to use this function otherwise will provide an error 
    def construct_prompt(self,prompt_input:str,role:str):
        pass

    

     

     
