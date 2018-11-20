

def generate_response_wrapper(data,
                              global_info_msgs=None,
                              global_warning_msgs=None,
                              global_error_msgs=None,
                              field_error_msgs=None):
    return {
       'data': data,
       'global_info_msgs': global_info_msgs,
       'global_warning_msgs': global_warning_msgs,
       'global_error_msgs': global_error_msgs,
       'field_error_msgs': field_error_msgs
    }


def serialize_user(user):
    return {"user_uuid": user.user_uuid,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username}


def serialize_user_item(user):
    return {"user_uuid": user.user_uuid,
            "first_name": user.first_name,
            "last_name": user.last_name}

def serialize_user_profile(user):
    return {"user_uuid": user.user_uuid,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username}


def serialize_codetable(codetable_data):
    data = []
    for item in codetable_data:
        data.append({"code": item.code.strip(), "description": item.description.strip()})
    return data


def serialize_authority(authorities):
    data = []
    for a in authorities:
        data.append(a.key)
    return data
