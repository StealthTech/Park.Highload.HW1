import os
import configparser


CONFIG_DEFAULT_PATH = '/etc/httpd.conf'
CONFIG_DEFAULT_IP_ADDR = '0.0.0.0'
CONFIG_DEFAULT_PORT = 80
CONFIG_DEFAULT_CPU_LIMIT = 4
CONFIG_DEFAULT_DOCUMENT_ROOT = '/var/www/html'


def get_configuration(filepath=None):
    if filepath is None:
        filepath = CONFIG_DEFAULT_PATH

    config = configparser.ConfigParser()
    if os.path.exists(filepath):
        config.read_file(open(filepath))

    options = {
        'ip_addr': config.get('main', 'ip_addr', fallback=CONFIG_DEFAULT_IP_ADDR),
        'document_root': config.get('main', 'document_root', fallback=CONFIG_DEFAULT_DOCUMENT_ROOT),
    }

    try:
        options['port'] = int(config.get('main', 'port'))
    except ValueError:
        options['port'] = CONFIG_DEFAULT_PORT

    try:
        options['cpu_limit'] = int(config.get('main', 'cpu_limit'))
    except ValueError:
        options['cpu_limit'] = CONFIG_DEFAULT_CPU_LIMIT

    return options
