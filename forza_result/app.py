from flask import Flask

from forza_result.api.v1 import bp as api_v1

app = Flask(__name__)
app.register_blueprint(api_v1, url_prefix='/api/v1')
