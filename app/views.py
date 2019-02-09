import os
from uuid import UUID

import celery
from celery.result import AsyncResult
from flask import Blueprint, current_app, request, Response, \
    after_this_request, send_from_directory
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from app import tasks, config
from app.utils import create_error_response, allowed_extension, \
    create_response, size_valid

operation_blueprint = Blueprint('operation', __name__, url_prefix='/operation')
status_blueprint = Blueprint('status', __name__, url_prefix='/status')


@operation_blueprint.route('/resize', methods=['POST'])
def process() -> Response:
    if 'file' not in request.files:
        current_app.logger.error("No file given: 'file' not in request.files")
        return create_error_response(422, 'No file given')

    file: FileStorage = request.files['file']

    if file.filename == '':
        current_app.logger.error("No file given: file.filename is ''")
        return create_error_response(422, 'No file given')

    data = request.values
    if not size_valid(data):
        return create_error_response(422, 'Invalid size')

    h = int(data['height'])
    w = int(data['width'])

    if file and allowed_extension(file.filename):
        task_id = celery.uuid()
        extension = file.filename.split('.')[1]
        filename = secure_filename(f'{task_id}.{extension}')
        file.save(os.path.join(config.upload_dir, filename))
        current_app.logger.info(f"File saved under name '{filename}'")

        task: celery.Task = tasks.resize_image.delay(filename, w, h)
        # Hack to be able to check the existence of the task:
        # PENDING task state is equal not existing task
        task.backend.store_result(task.id, None, 'SENT')

        return create_response(202,
                               status='accepted',
                               message='Upload complete',
                               task_id=task.id)
    else:
        current_app.logger.error(f'Wrong file extension: {file.filename}')
        return create_error_response(422, 'Invalid extension')


@operation_blueprint.route('/result/<uuid:task_id>', methods=['GET'])
def result(task_id: UUID) -> Response:
    task_result = AsyncResult(str(task_id))
    if task_result.state != 'SUCCESS':
        current_app.logger.warning(f'Requested result for unavailable task '
                                   f'with id {task_id}')
        return create_error_response(404, message='Result not found')
    else:
        path = task_result.get()
        current_app.logger.debug(path)

        @after_this_request
        def remove_file(response):
            current_app.logger.info(f'Removing file {path}')
            os.remove(path)
            return response

        directory = os.path.dirname(path)
        file = os.path.basename(path)
        current_app.logger.info(f'Sending file to client {directory}/{file}')
        return send_from_directory(directory, file)


@status_blueprint.route('/<uuid:task_id>', methods=['GET'])
def task_status(task_id: UUID) -> Response:
    task_result = AsyncResult(str(task_id))
    if task_result.state == 'PENDING':
        return create_error_response(404, message='Task not found')
    return create_response(200, status=task_result.state)
