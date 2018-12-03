from app import core


def debug_request(request):
    core.logger.debug("type=" + str(type(request)))
    for key, value in request.headers:
        core.logger.debug(str(key) + ":" + str(value))

    for field_name, value in request.form.items():
        core.logger.debug(str(field_name) + ":" + str(value))


def debug_response(response):

    core.logger.debug("type=" + str(type(response)))
    core.logger.debug("status_code=" + str(response.status_code))
    core.logger.debug("response.content_type=" + str(response.content_type))
    
    if response.data:
        core.logger.debug("Data=" + response.data.decode("utf-8"))
