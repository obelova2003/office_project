from rest_framework.exceptions import APIException


class PermissionDeniedException(APIException):
    status_code = 403
    default_detail = 'Вы не можете просматривать данные заявки!'
    

class DataBaseException(APIException):
    status_code = 400
    default_detail = 'Такой базы данных не существует или введены неверные данные!'
