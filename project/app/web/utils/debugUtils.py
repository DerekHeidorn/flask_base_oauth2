def debugRequest(request):
    print("type=" + str(type(request)))
    for key, value in request.headers:
        print(str(key) + ":" + str(value))

    for fieldname, value in request.form.items():
        print(str(fieldname) + ":" + str(value))

def debugResponse(response):
    
    print("type=" + str(type(response)))
    print("status_code=" + str(response.status_code))
    print("response.content_type=" + str(response.content_type))
    
    if(response.data):
        print("Data=" + response.data.decode("utf-8") )