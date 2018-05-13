from datetime import datetime

from utils import DATETIME_FORMAT_TEMPLATE


class HttpResponse:
    server_name = 'HomeworkServer'

    def __init__(self, protocol, status_code, content_type=None, content_length=None):
        self.protocol = protocol
        self.status_code = status_code
        self.content_type = content_type
        self.content_length = content_length
        self.date = datetime.utcnow().strftime(DATETIME_FORMAT_TEMPLATE)

    def __str__(self):
        response = '{} {}\r\n'.format(self.protocol, self.status_code)
        if self.content_type is not None:
            response += 'Content-Type: {}\r\n'.format(self.content_type)
        if self.content_length is not None:
            response += 'Content-Length: {}\r\n'.format(self.content_length)
        response += 'Date: {}\r\n'.format(self.date)
        response += 'Server: {}\r\n\r\n'.format(self.server_name)
        return response

    def as_bytes(self):
        return str(self).encode()
