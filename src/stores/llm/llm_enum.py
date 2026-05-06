from enum import Enum
class LLM_ENUMS(Enum):
    OPENAI="OPENAI"
    COHERE="COHERE"

class OpenAIEnums(Enum):
    SYSTEM="system"
    USER="user"
    ASSISTANT="assistant"

class Coher_Enums(Enum):
    SYSTEM="SYSTEM"
    USER="USER"
    ASSISTANT="CHATBOT"
    DOCUMENT="search_document"
    QUARY="search_query"

class Document_type(Enum):
    DOCUMENT="document"
    QUERY="query"


    


