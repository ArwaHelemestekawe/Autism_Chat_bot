from enum import Enum

class Responses(Enum):
    FILE_TYPE_NOT_SUPPORTED="NOT SUPPORTED FILE TYPE"
    FILE_TYPE_SUPPORTED="SUPPORTED FILE TYPE"
    FILE_UPLOADED_SUCCESSFULY="file uploaded"
    FILE_PROCESSING_FAILED="file_processing_failed"
    FILE_PROCESSING_SUCCESS="file_process_success"
    CHUNK_NOT_FOUNDED ="chunk not founded "
    FILE_NOT_FOUNDED_IN_DATA_BASE="file not founded in data base"
    

