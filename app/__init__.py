from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config
from datetime import timedelta
from flask_wtf import CSRFProtect
from flask_googlemaps import GoogleMaps
from app.constants import api_key
import os

app = Flask(__name__)
app.config.from_object(Config)
print(f"UPLOAD_FOLDER from config: {app.config.get('UPLOAD_FOLDER')}")  # Depuração

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
migrate = Migrate(app, db)
GoogleMaps(app, key=api_key)

# Verificação e criação do diretório de uploads
upload_folder = app.config.get('UPLOAD_FOLDER')
if not upload_folder:
    raise ValueError("UPLOAD_FOLDER não está configurado.")
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

from app import routes, models
