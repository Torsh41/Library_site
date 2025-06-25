from flask import Blueprint
moderation = Blueprint('moderation', __name__)
from . import views
