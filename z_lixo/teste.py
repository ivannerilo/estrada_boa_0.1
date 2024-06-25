from app import db
from app.models import Report

reports = Report.query.all()


