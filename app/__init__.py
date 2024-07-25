from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_caching import Cache
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import atexit
import os

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
cache = Cache()
scheduler = BackgroundScheduler()

# def create_app():
#     app = Flask(__name__)
#     app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/profile_pics')
#     app.config['SECRET_KEY'] = 'your_secret_key'
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

#     db.init_app(app)
#     login_manager.init_app(app)
#     login_manager.login_view = 'login'

#     from app.routes import main
#     app.register_blueprint(main)

#     with app.app_context():
#         db.create_all()

#     return app

def send_daily_reminders():
    from app.models import User, AdRequest
    from app.email import send_reminder_email
    
    influencers = User.query.filter_by(role='influencer').all()
    for influencer in influencers:
        pending_ad_requests = AdRequest.query.filter_by(influencer_id=influencer.id, status_influencer='Pending').count()
        if pending_ad_requests > 0:
            send_reminder_email(influencer.email)

def send_monthly_reports():
    from app.models import User
    from app.email import send_report_email
    
    sponsors = User.query.filter_by(role='sponsor').all()
    for sponsor in sponsors:
        send_report_email(sponsor.email)

def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/profile_pics')
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['MAIL_SERVER'] = 'mail.smtp2go.com'
    app.config['MAIL_PORT'] = 2525
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = '22f1000811@ds.study.iitm.ac.in'
    app.config['MAIL_PASSWORD'] = 'RzpNb8JWsyuOQpAa'
    app.config['MAIL_DEFAULT_SENDER'] = '22f1000811@ds.study.iitm.ac.in'
    app.config['CACHE_TYPE'] = 'SimpleCache'
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    mail.init_app(app)
    cache.init_app(app)
    
    from app.routes import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    scheduler.add_job(func=send_daily_reminders, trigger='interval', days=1, start_date=datetime.now())
    scheduler.add_job(func=send_monthly_reports, trigger='cron', day=1, hour=0, minute=0)
    scheduler.start()
    
    atexit.register(lambda: scheduler.shutdown())

    return app