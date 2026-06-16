from enum import Enum

class Responses(Enum):
    FILE_TYPE_NOT_SUPPORTED="NOT SUPPORTED FILE TYPE"
    FILE_TYPE_SUPPORTED="SUPPORTED FILE TYPE"
    FILE_UPLOADED_SUCCESSFULY="file uploaded"
    FILE_PROCESSING_FAILED="file_processing_failed"
    FILE_PROCESSING_SUCCESS="file_process_success"
    CHUNK_NOT_FOUNDED ="chunk not founded "
    FILE_NOT_FOUNDED_IN_DATA_BASE="file not founded in data base"
    CATEGORY_NOT_FOUND="category_not_found"
    CHUNK_VICTORIZED_CORRECTLY="chunk victorized correctly and inserted"
    CHUNK_VICTORIZED_failed="chunk victorizing and insertion failed"
    QUERY_VECTOR_IS_NOT_FOUNDED="query vector is not founded"
    QUERY_VECTOR_IS_FOUNDED="query vector is  founded"
    SEARCH_QUERY_SUCCESS="SEARCH SUCCES"
    SEARCH_QUERY_Fail="SEARCH fail"
    ANSWER_RAG_FAILED="answer_failed"
    ANSWER_RAG_success="answer_success"






    

