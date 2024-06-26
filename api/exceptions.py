from rest_framework.exceptions import APIException


class Exception(APIException):
    status_code = 403
    default_detail = 'Вы не можете просматривать данные заявки!'
    