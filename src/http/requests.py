from urllib.parse import unquote, urlparse


class HttpRequest:
    def __init__(self, method, protocol, url):
        self.method = method
        self.protocol = protocol
        self.url = unquote(urlparse(url).path)

    @classmethod
    def from_string(cls, request_str):
        request_lines = request_str.split('\n')
        try:
            method, url, protocol = request_lines[0].split()
        except ValueError:
            return None
        return cls(method, protocol, url)
