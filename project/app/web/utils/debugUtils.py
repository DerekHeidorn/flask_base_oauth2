

def debug_request(request):
    print("type=" + str(type(request)))
    for key, value in request.headers:
        print(str(key) + ":" + str(value))

    for field_name, value in request.form.items():
        print(str(field_name) + ":" + str(value))


def debug_response(response):
    
    print("type=" + str(type(response)))
    print("status_code=" + str(response.status_code))
    print("response.content_type=" + str(response.content_type))
    
    if response.data:
        print("Data=" + response.data.decode("utf-8") )