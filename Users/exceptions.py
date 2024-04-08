from rest_framework import status
from rest_framework.exceptions import APIException

class ModelExecutionExceptions():
    class IncorrectModelPath(APIException):
        status_code = status.HTTP_404_NOT_FOUND
        default_detail = 'The model path was not correct'
        default_code = 'not_correct_path'

    class IncorrectFileExtension(APIException):
        status_code = status.HTTP_400_BAD_REQUEST
        default_detail = 'Only .xmile files are allowed'
        default_code = 'extension_not_allowed'

    class IncorrectModelDefinition(APIException):
        status_code = status.HTTP_400_BAD_REQUEST
        default_detail = 'The model was not correctly defined'
        default_code = 'model_bad_defined'
    
    class IncorrectExcelFile(APIException):
        status_code = status.HTTP_400_BAD_REQUEST
        default_detail = 'The excel file defining a lookup function was not correct'
        default_code = 'incorrect_excel_file'
    
    class IncorrectExcelFileExtension(APIException):
        status_code = status.HTTP_400_BAD_REQUEST
        default_detail = 'Only .xlsx and .xls files are allowed as lookup functions'
        default_code = 'extension_not_allowed'

class ModelExceptions():
    
    class NotAllowedAccess(APIException):
        status_code = status.HTTP_401_UNAUTHORIZED
        default_detail = 'You are not allowed to access this model'
        default_code = 'not_allowed_access'
