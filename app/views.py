import os
from uuid import UUID

import celery
from flask import (
    Blueprint, current_app, request, Response,
    after_this_request, send_from_directory
)
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from app import tasks, config
from app.utils import (
    create_error_response, allowed_extension, create_response, size_valid
)

operation_blueprint = Blueprint('operation', __name__, url_prefix='/operation')
status_blueprint = Blueprint('status', __name__, url_prefix='/status')


@operation_blueprint.route('/resize', methods=['POST'])
def process() -> Response:
    current_app.logger.info('Attempt to create resizing task')
    if 'file' not in request.files:
        current_app.logger.warning(
            "No file given: 'file' not in request.files")
        return create_error_response(422, 'No file given')

    current_app.logger.info('Reading file')
    file: FileStorage = request.files['file']

    if file.filename == '':
        current_app.logger.warning("No file given: file.filename is ''")
        return create_error_response(422, 'No file given')

    current_app.logger.info('Reading resize parameters')
    data = request.values
    if not size_valid(data):
        current_app.logger.warning("File size parameters are invalid")
        return create_error_response(422, 'Invalid size')

    h = int(data['height'])
    w = int(data['width'])

    if file and allowed_extension(file.filename):
        current_app.logger.info('Saving file')
        task_id = celery.uuid()
        extension = file.filename.split('.')[1]
        filename = secure_filename(f'{task_id}.{extension}')
        file.save(os.path.join(config.upload_dir, filename))
        current_app.logger.info(f"File saved under name '{filename}'")

        current_app.logger.info('Creating celery task')
        task: tasks.celery.Task = tasks.resize_image.apply_async(
            args=[filename, w, h], task_id=task_id)
        # Hack to be able to check the existence of the task:
        # PENDING task state is equal not existing task
        task.backend.store_result(task.id, None, 'SENT')

        current_app.logger.info('Request accepted, task was sent into queue')
        return create_response(202,
                               status='accepted',
                               message='Upload complete',
                               task_id=task.id)
    else:
        current_app.logger.warning(f'Wrong file extension: {file.filename}')
        return create_error_response(422, 'Invalid extension')


@operation_blueprint.route('/result/<uuid:task_id>', methods=['GET'])
def result(task_id: UUID) -> Response:
    current_app.logger.info(f'Attempt to get task result with id: {task_id}')

    task_result = tasks.celery.AsyncResult(str(task_id))
    state = 'PENDING'
    try:
        state = task_result.state
    except AttributeError as e:
        current_app.logger.critical(f'Celery backend disabled: {e}')

    if state != 'SUCCESS':
        current_app.logger.info(f'Attempt rejected: the task does not exist or'
                                f' is not completed yet')

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
    current_app.logger.info(f'Attempt to get task status with id: {task_id}')

    task_result = tasks.celery.AsyncResult(str(task_id))
    state = 'PENDING'

    try:
        state = task_result.state
    except AttributeError as e:
        current_app.logger.critical(f'Celery backend disabled: '
                                    f'{e}')

    if state == 'PENDING':
        current_app.logger.info(f'Attempt rejected: the task does not exist')
        return create_error_response(404, message='Task not found')

    current_app.logger.info(f'Returned state ({state}) '
                            f'of task with id {task_id}')
    return create_response(200, status=state)
