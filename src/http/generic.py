ALLOWED_METHODS = ['GET', 'HEAD']


class MimeTypeManager:
    def __init__(self):
        self.__map = {
            'css': 'text/css',
            'gif': 'image/gif',
            'html': 'text/html',
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'js': 'text/javascript',
            'png': 'image/png',
            'swf': 'application/x-shockwave-flash',
            'txt': 'text/txt',
        }
        self.__default = 'text/plain'

    def resolve(self, extension):
        if len(extension) > 0 and extension[0] == '.':
            extension = extension[1:]
        return self.__map.get(extension, self.__default)
