# app/email.py

from flask_mail import Message
from app import mail
# from app.models import User, Campaign, AdRequest

def send_reminder_email(recipient):
    msg = Message('Daily Reminder', sender='22f1000811@ds.study.iitm.ac.in', recipients=[recipient])
    msg.body = 'You have pending ad requests. Please visit the platform to accept or reject them.'
    mail.send(msg)

def send_report_email(recipient):
    from app.models import User, Campaign, AdRequest
    from flask import render_template

    # Retrieve the sponsor's campaigns and ad requests
    sponsor = User.query.filter_by(email=recipient).first()
    campaigns = Campaign.query.filter_by(user_id=sponsor.id).all()
    # ad_requests = AdRequest.query.filter_by(sponsor_id=sponsor.id).all()
    ad_requests = AdRequest.query.join(Campaign, AdRequest.campaign_id == Campaign.id)\
    .filter(
        Campaign.user_id == sponsor.id
        # AdRequest.status_sponsor == 'Pending', AdRequest.status_influencer != 'Rejected'
    ).all()

    # Generate the report content
    report_content = render_template('monthly_report.html', sponsor=sponsor, campaigns=campaigns, ad_requests=ad_requests)
    
    msg = Message('Monthly Activity Report', sender='22f1000811@ds.study.iitm.ac.in', recipients=[recipient])
    msg.html = report_content
    mail.send(msg)

