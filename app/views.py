import os

from flask import Blueprint, current_app, request, Response
from werkzeug.utils import secure_filename

from app.utils import create_error_response, allowed_extension, \
    create_response, size_valid

blueprint = Blueprint('operation', __name__, url_prefix='/operation')


@blueprint.route('/resize', methods=['POST'])
def process() -> Response:
    if 'file' not in request.files:
        current_app.logger.error("No file given: 'file' not in request.files")
        return create_error_response(422, 'No file given')

    file = request.files['file']

    if file.filename == '':
        current_app.logger.error("No file given: file.filename is ''")
        return create_error_response(422, 'No file given')

    data = request.values
    if not size_valid(data):
        return create_error_response(422, 'Invalid size')

    if file and allowed_extension(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        current_app.logger.info(f"File saved under name '{filename}'")

        return create_response(200,
                               status='success',
                               message='Upload complete',
                               task_id=-1)
    else:
        current_app.logger.error(f'Wrong file extension: {file.filename}')
        return create_error_response(422, 'Invalid extension')
