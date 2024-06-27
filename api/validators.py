import ipaddress

from django.core.exceptions import ValidationError


def validate_host(host):
    try:
        ipaddress.ip_address(host)
    except:
        raise ValidationError('не подходит')
    return host