from flask import Flask

app = Flask(__name__)

app.config.from_object("config.DevelopmentConfig")
app.config['INITIAL_FILE_UPLOADS'] = 'app/static/uploads' # Define it here

