import json
from werkzeug.exceptions import HTTPException
from flask import jsonify, abort, Response
from project.app.web.utils import serializeUtils
import traceback


def handle_error(e):
    traceback.print_exc()
    print("Exception:" + str(type(e)) + " msg=" + str(e))
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code


def handle_validation_error(e):
    print("ValidationError=" + str(e))
    print("err.messages=" + str(e.messages))
    print("err.valid_data=" + str(e.valid_data))
    resp = _handle_schema_validation_error(e.messages)
    return resp


def _handle_schema_validation_error(error_messages):

    field_error_msgs = []
    for k in error_messages:
        print(k + ", " + str(error_messages[k]))
        field_error_msgs.append({k: error_messages[k]})
    r = Response()
    r.status_code = 400
    r.content_type = 'application/json'
    r.data = json.dumps(serializeUtils.generate_response_wrapper(None, field_error_msgs=field_error_msgs))
    return r


def handle_http_exception(e):
    print("HTTPException=" + str(e))
    return jsonify(error=str(e)), e.code
