import os

from core import start_server
from utils.config import get_configuration

if __name__ == '__main__':
    startup_mode = os.environ.get('startup_mode', 'docker')
    filepath = 'conf/server.conf' if startup_mode == 'dev' else None

    options = get_configuration(filepath)
    start_server(options)
