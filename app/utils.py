from flask import Response, make_response, jsonify, current_app


def size_valid(data: dict) -> bool:
    if data and 'height' in data and 'width' in data:
        h = int(data['height'])
        w = int(data['width'])
        if 0 < h <= 9999 and 0 < w < 9999:
            return True
        else:
            current_app.logger.error(f"Invalid size parameters provided: "
                                     f"wrong h: {h} "
                                     f"or w: {w}")
    else:
        current_app.logger.error(f'Invalid size parameters provided: '
                                 f'wrong json {data}')
    return False


def create_response(code: int = 204, **kwargs) -> Response:
    """
    Creating JSON response from key word arguments

    :param code: Status code of response
    :param kwargs: key=value args to create json with
    :return: Response object with given status code and arguments
    """
    return make_response(jsonify(kwargs), code)


def create_error_response(code: int, message: str) -> Response:
    return create_response(code, result='error', message=message)


def allowed_extension(file_name: str) -> bool:
    return '.' in file_name and file_name.split('.')[1].lower() in \
           current_app.config.get('ALLOWED_EXTENSIONS')
