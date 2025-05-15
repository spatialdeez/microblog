# Microblog
Simple microblog web application made in the month and year of May 2025

# How to use
### 1. Clone the repository (Copying the files)

```bash
git clone https://github.com/spatialdeez/microblog
```

### 2. Create and activate virtual environment
Enter the following lines:
```bash
$ cd your_absolute_path/microblog
$ python -m venv venv
$ venv\Scripts\activate
```

### 3. Install dependencies
Type this in your command prompt/terminal
```bash
$ pip install -r requirements.txt
```

### 4. Set enviornment variables (If variables not copied over)
Type this in your command prompt/terminal before starting the flask applications
```bash
$ set FLASK_APP=microblog.py
```

### 5. Database setup
You will need a database to handle user and posts
Enter the following lines:
```bash
(venv) $ flask db init
(venv) $ flask db migrate -m "Database setup"
(venv) $ flask db upgrade
```

### Complete setup with config.py
Make a new config.py file in the root directory (mainly just microblog file)
Open, edit the file, and then copy this code in:
```bash
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'test-mb'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    POSTS_PER_PAGE = 10
    MAIL_SERVER = '<your-chosen-server>'
    MAIL_PORT= 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = '<your-email-address>'
    MAIL_PASSWORD = '<your-email-password>'
    LANGUAGES = ['en, es']
```
NOTE: For the variables MAIL_SERVER, MAIL_USERNAME, MAIL_PASSWORD, please edit it 
to your actual email address and password, and your chosen mail server
It is not recommended to use Gmail, Yahoo! or any other major email providers as
there are restrictions set on how you can send your emails. Use a private domain if possible.

### 7. Run the Flask application!
Type this in your command prompt/terminal
```bash
$ (venv) flask run
```

### Legend:
$ - stands for command prompt (e.g. C:\Users\example>) <br/>
$ (venv) - stands for command prompt running in virtual environment (e.g. (venv) C:\Users\example>)