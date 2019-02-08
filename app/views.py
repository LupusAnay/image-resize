import os

from flask import Blueprint, current_app, request, Response
from werkzeug.utils import secure_filename

from app.utils import create_error_response, allowed_extension, create_response

blueprint = Blueprint('operation', __name__, url_prefix='/operation')


@blueprint.route('/resize', methods=['POST'])
def process() -> Response:
    if 'file' not in request.files:
        current_app.logger.error('No file given')
        return create_error_response(422, 'No file given')
    file = request.files['file']
    if file.filename == '':
        return create_error_response(422, 'No file given')

    if file and allowed_extension(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        return create_response()
