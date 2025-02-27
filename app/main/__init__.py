from flask import Blueprint
main = Blueprint('main', __name__)
TOP_BOOKS_COUNT = 3
BOOKS_MAINTAINING_PER_PAGE = 20
MAX_PRIVATE_CHATS_PER_USER = 10
MAX_INVITATIONS_PER_CHAT = 30
ELEMS_COUNT = 8
USERS_COUNT = 4
months_dict = {
    1: 'января',
    2: 'февраля',
    3: 'марта',
    4: 'апреля',
    5: 'мая',
    6: 'июня',
    7: 'июля',
    8: 'августа',
    9: 'сентября',
    10: 'октября',
    11: 'ноября',
    12: 'декабря'
}
from . import views, errors, events, events_of_private_chats