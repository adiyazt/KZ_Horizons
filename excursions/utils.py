from datetime import datetime
from excursions.models import (
                                Excursion, Attraction,
                                exc_kinds, exc_types, transport, User, Booking
                            )


def upload_photo(photo, id: str):
    _filename = str(photo)
    if _filename.split('.')[-1] in ('jpg', 'png', 'jpeg'):
        short = f'img/images/excursions/{id}.{_filename.split(".")[-1]}'
        _path = f'users/static/{short}'

        with open(_path, 'wb+') as _file:
            for chunk in photo.chunks():
                _file.write(chunk)
        
        return short
    

def get_type(excursion):
    return exc_types[int(excursion.type)-1][1]

def get_kind(excursion):
    return exc_kinds[int(excursion.kind)-1][1]

def get_transport(excursion):
    return transport[int(excursion.transport)-1][1]