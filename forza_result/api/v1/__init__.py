import flask
import logging
import tempfile
import pathlib
from flask import request, abort, make_response
from flask import jsonify, redirect, url_for
from functools import wraps
from forza_result.api import CustomBlueprint
from forza_result import convert

bp = CustomBlueprint('api', __name__)

logger = logging.getLogger('ocr')
logger.setLevel(logging.INFO)

###############################################################################
def custom_error(message, status_code):
    msg = dict(message=message)
    return make_response(jsonify(msg), status_code)


###############################################################################
def result(f):
    @wraps(f)
    def func(*args, **kwargs):
        try:
            r = f(*args, **kwargs)
            return jsonify(r)
        except Exception as e:
            return custom_error(str(e), status_code=500)
    return func


###############################################################################
@bp.route('/ocr', methods=('GET', 'POST'))
@result
def schedules():
    if request.method == 'POST':
        file = request.files['file']
        tempdir = tempfile.gettempdir()
        filepath = str(pathlib.Path(tempdir, 'temp.png'))
        file.save(filepath)

        logger.info('start ocr')
        data = convert(filepath, '')
        logger.info('done ocr')
        return data
