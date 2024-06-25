from flask import Flask, render_template, request, redirect, url_for, session, flash
from app import app, db
from app.models import User, Report, DamageMedia, ProblemMedia
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from app.forms import LoginForm, RegisterForm, ReportForm, CSRFForm
from flask_wtf.csrf import CSRFProtect
from app.constants import PROBLEM_TYPES, DAMAGE_TYPES, api_key
from flask_googlemaps import Map
from flask import Blueprint, g, render_template
from markupsafe import Markup
from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov'}

csrf = CSRFProtect(app)

@app.route('/')
@app.route('/index')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=session.get('username'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session.permanent = True
            next_page = request.args.get('next')
            return redirect(next_page or url_for('report'))
        else:
            flash('Credenciais inválidas!', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        confirmation = form.confirmation.data

        if password != confirmation:
            flash('Digite a mesma senha nos dois formularios!', 'danger')
            return redirect(url_for('register'))
        
        password_hash = generate_password_hash(password)
        
        new_user = User(username=username, email=email, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registro bem-sucedido! Faça login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('Você saiu da sua conta.', 'success')
    return redirect(url_for('login'))
        
@app.route('/report', methods=['GET', 'POST'])
@csrf.exempt
@login_required
def report():
    form = ReportForm()
    if form.validate_on_submit():
        try:
            description = form.description.data
            latitude = float(form.latitude.data)
            longitude = float(form.longitude.data)
            damage_type = form.damage_type.data
            
            print(f'Received data: description={description}, latitude={latitude}, longitude={longitude}, damage_type={damage_type}')

            report = Report(description=description, latitude=latitude, longitude=longitude, damage_type=damage_type, user_id=session['user_id'])
            db.session.add(report)
            db.session.commit()
            
            flash('Problema reportado com sucesso!', 'success')
        except Exception as e:
            print(f'Error: {e}')
            flash('Erro ao reportar problema. Tente novamente.', 'danger')
            return redirect(url_for('report'))
    else:
        print('Form did not validate')
        print(form.errors)

    reports = Report.query.all() # Puxa todos os reports na database para mostrar no mapa!
    reports_data = [
        {
            "id": report.id,
            "user_id": report.user_id,
            "description": report.description,
            "latitude": report.latitude,
            "longitude": report.longitude,
            "timestamp": report.timestamp.isoformat(),
            "damage_type": report.damage_type
        } 
        for report in reports
    ]
    
    return render_template('report.html', form=form, title='Reportar Problema', problem_types=PROBLEM_TYPES, damage_types=DAMAGE_TYPES, reports=reports_data)

@app.route('/user_reports')
@login_required
def user_reports():
    user_id = session['user_id']
    user = User.query.get(user_id)
    reports = user.reports.all()
    return render_template('myreports.html', reports=reports)

@app.route('/report_details/<int:report_id>', methods=['GET'])
@login_required
def report_details(report_id):
    report = Report.query.get_or_404(report_id)
    csrf_form = CSRFForm()
    return render_template('report_details.html', report=report, form=csrf_form, api_key=api_key)


@app.route('/delete_report/<int:report_id>', methods=['POST'])
@login_required
def delete_report(report_id):
    report = Report.query.get_or_404(report_id)
    if report.user_id != session['user_id']:
        flash('Você não tem permissão para deletar este relatório.', 'danger')
        return redirect(url_for('user_reports'))
    
    db.session.delete(report)
    db.session.commit()
    
    flash('Relatório deletado com sucesso!', 'success')
    return redirect(url_for('user_reports'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_files/<int:report_id>', methods=['POST'])
@login_required
def upload_files(report_id):
    if 'problem_media' not in request.files or 'damage_media' not in request.files:
        return redirect(request.url)

    problem_media_files = request.files.getlist('problem_media')
    damage_media_files = request.files.getlist('damage_media')

    for file in problem_media_files + damage_media_files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Salve o caminho do arquivo no banco de dados, associando-o ao relatório
            save_file_to_db(report_id, filename, 'problem' if file in problem_media_files else 'damage')

    return redirect(url_for('report_details', report_id=report_id))

def save_file_to_db(report_id, filename, file_type):
    # Função para salvar informações do arquivo no banco de dados
    media = ProblemMedia(report_id=report_id, file_path=filename) if file_type == 'problem' else DamageMedia(report_id=report_id, file_path=filename)
    db.session.add(media)
    db.session.commit()









