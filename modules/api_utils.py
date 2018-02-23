from gluon import current

def json_response(api_name, data, code=200, version="1"):
    """
    Returns a structured dictionary for JSON API response, also sets response status code
    :param api_name: Current API name
    :param data: Data object to return
    :param code: response status code
    :param version: API version
    :return: dictionary for JSON API response
    """
    response = {
        "header": {
            "application": current.request.application,
            "api": api_name,
            "version": version
        }
    }
    if 200 <= code < 300:
        response['data'] = data
    else:
        current.response.status = code
        response['message'] = data
        response['code'] = code
    return response
