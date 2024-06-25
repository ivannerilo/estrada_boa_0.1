import os
from datetime import timedelta

class Config:
    SECRET_KEY = 'e433189b365b604b8185915d6f174'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///estrada_boa.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    GOOGLEMAPS_KEY = 'AIzaSyDVkOkMjhCcbVkbchAAYsN-_Tg12xDrfVA'
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
