import json
from flask import abort, Response
from project.app.web.utils import serializeUtils


def handle_schema_validation_error(error_messages):

    field_error_msgs = []
    for k in error_messages:
        print(k + ", " + str(error_messages[k]))
        field_error_msgs.append({k: error_messages[k]})
    r = Response()
    r.status_code = 400
    r.content_type = 'application/json'
    r.data = json.dumps(serializeUtils.generate_response_wrapper(None, field_error_msgs=field_error_msgs))
    return r
