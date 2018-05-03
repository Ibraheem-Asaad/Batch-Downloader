"""Credentials and configurations for downloader module"""

REQUIRES_AUTHORIZATION = False
LOGIN_URL = ''
LOGIN_FORM_INDEX = 0
USER_FIELD_NAME = ''
USERNAME = ''
PASS_FIELD_NAME = ''
PASSWORD = ''
LOGOUT_URL = ''

TARGET_URLS = {
    r'https://www.jlpt.jp/e/samples/sample12.html'
}
TARGET_FOLDER = r'/home/ibrahiem/Desktop/JLPT'

MAX_FILES = 100
EXTENSIONS = {'pdf', 'mp3'}
NAME_PATTERN = '*N5*'  # '*' for no restrictions
REQUEST_CONFIRMATION = False


def name_mapping(name, file_num):
    """Changes each downloaded file name accordingly"""
    # manipulate name patterns - use file_num for incremental numbering:
    return name \
        .replace('%20', ' ') \
        .replace('_', ' ') \
        .replace('-', ' ')
