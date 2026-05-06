from src.stores.llm.LLMinterface import LLMInterface
from src.stores.llm.llm_enum import OpenAIEnums,LLM_ENUMS
from openai import OpenAI
import logging

class OpenAIProvider(LLMInterface):
    def __init__(self,api_key:str,api_url:str=None,
                 defualt_input_max_tokens:int=1000,
                 defualt_output_max_tokens:int=1000,
                 defualt_generation_temp=0.5):
        self.api_key=api_key
        self.api_url=api_url
        self.defualt_input_max_tokens=defualt_input_max_tokens
        self.defualt_output_max_tokens=defualt_output_max_tokens
        self.defualt_generation_temp=defualt_generation_temp

        self.generation_model_id=None
        self.embedding_model_id=None
        self.vector_size=None

        self.client=OpenAI(
            api_key=self.api_key,
            api_url=self.api_url
        )
        self.tempreture=0.5
        self.logger=logging.getLogger(__name__)

# why i just not but as an argument in the init constructor ? abo bakr said that we mightnot want the open ai to be the only 
# model we want to use , putting it in init force the programe to use it at the run time with out any ability to change it 
# so it is better to but it in different function .
    def set_generation_model(self,model_id:str):
        self.generation_model_id=model_id


    def set_embedding_model(self,model_id:str,embeding_size:int):
        self.embedidng_model_id=model_id
        self.vector_size=embeding_size


    def generate_text(self,prompt_input:str,chat_history:list=[],max_output_tokens:int=None,tempreture:float=0.5):
        if not self.client:
            self.logger.error("Embedding model is not set error in passing client info")
            return None
        if not self.generation_model_id:
            self.logger.error("generation model should be provided")
            return None
        max_output_tokens=max_output_tokens if max_output_tokens  else self.defualt_output_max_tokens
        


        chat_history.append(
            self.construct_prompt(prompt_input=prompt_input,role=OpenAIEnums.USER.value)
        )
        
        response=self.client.chat.completions.create(
            model=self.generation_model_id,
            messages=chat_history,
            max_tokens=self.defualt_output_max_tokens,
            temperature=self.tempreture
        )

        if not response or not response.choices or len(response.choices)==0 or not response.choices[0]:
            self.logger.error("error while generating text with open AI")
            return None
        return response.choices[0].message["content"]



        



    def embed_text(self,text:str,document_type=None):
        if not self.client:
            self.logger.error("Embedding model is not set error in passing client info")
            return None
        if not self.embedding_model_id:
            self.logger.error("embedding model id is not founded")
            return None
        
        response=self.client.embeddings.create(
            model=self.embedding_model_id,
            input=text,
        )
        if not response or not response.data or len(response.data) == 0 or not response.data[0].embedding:
            self.logger.error("Error while embedding text with OpenAI")
            return None
        return response.data[0].embedding

    

    def construct_prompt(self,prompt_input:str,role:str):
        return{
            "role":role,
            "content":self.process_text(text=prompt_input)
        }
        

    def process_text(self,text:str):
        return text[:self.defualt_input_max_tokens]


     

"""from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role":"system","content":"You are a helpful assistant."},
        {"role":"user","content":"Who won the world series in 2020?"},
        {"role":"assistant","content":"The Los Angeles Dodgers won the World Series in 2020."},
        {"role":"user","content":"Where was it played?"}
    ]
)
"""

        

        

