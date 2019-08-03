from flask import Flask
from pyfladesk import init_gui
from models import *
import os

'''
Find file name
'''

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
Base_path, app_name = os.path.split(APP_ROOT)
file_name = "/inventory.db"
# DB_LOCATION = APP_ROOT + file_name

SQLITE_PATH = Base_path + file_name

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///'+ SQLITE_PATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


from forms import *
from helper import *
from views import *

with app.test_request_context():
        db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
    # init_gui(app, width=900, height=600, window_title="SohozHisab", argv=None)



