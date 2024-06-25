Set-ExecutionPolicy RemoteSigned -Scope Process

.\venv\Scripts\Activate

flask db init
flask db migrate -m "Initial migration."
flask db upgrade


secret key = e433189b365b604b8185915d6f174


