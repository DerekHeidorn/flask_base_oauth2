import json
from flask import Response


def generate_response_wrapper(data,
                              global_success_msgs=None,
                              global_info_msgs=None,
                              global_warning_msgs=None,
                              global_error_msgs=None,
                              field_error_msgs=None):
    return {
       'data': data,
       'global_success_msgs': global_success_msgs,
       'global_info_msgs': global_info_msgs,
       'global_warning_msgs': global_warning_msgs,
       'global_error_msgs': global_error_msgs,
       'field_error_msgs': field_error_msgs
    }


def add_global_success_msg(response_wrapper, msg):
    return add_global_msg(response_wrapper, 'global_success_msgs', msg)


def add_global_info_msg(response_wrapper, msg):
    return add_global_msg(response_wrapper, 'global_info_msgs', msg)


def add_global_warning_msg(response_wrapper, msg):
    return add_global_msg(response_wrapper, 'global_warning_msgs', msg)


def add_global_error_msg(response_wrapper, msg):
    return add_global_msg(response_wrapper, 'global_error_msgs', msg)


def add_global_msg(response_wrapper, key, msg):
    if response_wrapper[key] is None:
        msgs = list()
        msgs.append(msg)
        response_wrapper[key] = msgs

    else:
        response_wrapper[key].append(msg)

    return response_wrapper


def handle_schema_validation_error(error_messages):

    field_error_msgs = []
    for k in error_messages:
        field_error_msgs.append({k: error_messages[k]})
    r = Response()
    r.status_code = 400
    r.content_type = 'application/json'
    r.data = json.dumps(generate_response_wrapper(None, field_error_msgs=field_error_msgs))
    return r
