from flask import Response, make_response, jsonify, current_app


def create_response(code: int = 204, **kwargs) -> Response:
    """
    Creating JSON response from key word arguments

    :param code: Status code of response
    :param kwargs: key=value args to create json with
    :return: Response object with given status code and arguments
    """
    return make_response(jsonify(kwargs), code)


def create_error_response(code: int, reason: str) -> Response:
    return create_response(code, result='error', message=reason)


def allowed_extension(file_name: str) -> bool:
    current_app.logger.error('Wrong file extension')
    return '.' in file_name and file_name.split('.')[1].lower() in \
           current_app.config.get('ALLOWED_EXTENSIONS')
