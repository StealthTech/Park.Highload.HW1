from . import HttpResponse


HTTP_STATUS_OK = '200 OK'
HTTP_STATUS_BAD_REQUEST = '400 Bad Request'
HTTP_STATUS_FORBIDDEN = '403 Forbidden'
HTTP_STATUS_NOT_FOUND = '404 Not Found'
HTTP_STATUS_METHOD_NOT_ALLOWED = '405 Method Not Allowed'
HTTP_PROTOCOL_DEFAULT = 'HTTP/1.1'


class HttpResponseOk(HttpResponse):
    def __init__(self, protocol, content_type, content_length):
        super(HttpResponseOk, self).__init__(protocol, HTTP_STATUS_OK, content_type, content_length)


class HttpResponseForbidden(HttpResponse):
    def __init__(self, protocol=HTTP_PROTOCOL_DEFAULT):
        super(HttpResponseForbidden, self).__init__(protocol, HTTP_STATUS_FORBIDDEN)


class HttpResponseNotFound(HttpResponse):
    def __init__(self, protocol=HTTP_PROTOCOL_DEFAULT):
        super(HttpResponseNotFound, self).__init__(protocol, HTTP_STATUS_NOT_FOUND)


class HttpResponseMethodNotAllowed(HttpResponse):
    def __init__(self, protocol=HTTP_PROTOCOL_DEFAULT):
        super(HttpResponseMethodNotAllowed, self).__init__(protocol, HTTP_STATUS_METHOD_NOT_ALLOWED)


class HttpResponseBadRequest(HttpResponse):
    def __init__(self, protocol=HTTP_PROTOCOL_DEFAULT):
        super(HttpResponseBadRequest, self).__init__(protocol, HTTP_STATUS_BAD_REQUEST)
