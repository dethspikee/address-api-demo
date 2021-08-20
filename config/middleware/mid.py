def add_indentation(get_response):

    def middleware(request):
        # add indentation
        request.META["HTTP_ACCEPT"] = "application/json; indent=4"

        response = get_response(request)
        return response

    return middleware
