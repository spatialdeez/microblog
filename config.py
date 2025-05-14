import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'oh-what-the-flipp'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    POSTS_PER_PAGE = 10
    MAIL_SERVER = 'in-v3.mailjet.com'
    MAIL_PORT= 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'donotreply20353487@gmail.com'
    MAIL_PASSWORD = 'f3006eaa180f5c8de3d8f825b5dc8794'