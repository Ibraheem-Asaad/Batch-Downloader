"""Download all files of a certain file extension from a webpage"""

import os
import requests
import urllib.parse as urlparse
import urllib.request as urlrequest
from fnmatch import fnmatch
from lxml import html
from configs import REQUIRES_AUTHORIZATION, LOGIN_URL, LOGIN_FORM_INDEX, USER_FIELD_NAME, \
    USERNAME, PASS_FIELD_NAME, PASSWORD, LOGOUT_URL, TARGET_URLS, TARGET_FOLDER, \
    MAX_FILES, EXTENSIONS, REQUEST_CONFIRMATION, NAME_PATTERN, name_mapping


def login(session):
    # TODO: Test downloads with credentials
    """Login to the website"""
    response = session.get(LOGIN_URL)
    response.raise_for_status()
    login_form = html.fromstring(response.content).forms[LOGIN_FORM_INDEX]
    payload = dict(login_form.fields)
    payload[USER_FIELD_NAME] = USERNAME
    payload[PASS_FIELD_NAME] = PASSWORD
    response = session.post(LOGIN_URL, payload)
    response.raise_for_status()


def iri_to_uri(iri, encoding='Latin-1'):
    """Takes a Unicode string that can contain an IRI and emits a URI."""
    scheme, authority, path, query, frag = urlparse.urlsplit(iri)
    scheme = scheme.encode(encoding)
    if ":" in authority:
        host, port = authority.split(":", 1)
        authority = host.encode('idna') + ":%s" % port
    else:
        authority = authority.encode(encoding)
    path = urlparse.quote(path.encode(encoding), safe="/;%[]=:$&()+,!?*@'~")
    query = urlparse.quote(query.encode(encoding), safe="/;%[]=:$&()+,!?*@'~")
    frag = urlparse.quote(frag.encode(encoding), safe="/;%[]=:$&()+,!?*@'~")
    return urlparse.urlunsplit((scheme.decode('utf-8'), authority.decode('utf-8'), path, query, frag))


def file_name_match(file_name):
    """returns if the file_name matches requirements (extension and pattern)"""
    return file_name.split('.')[-1] in EXTENSIONS and fnmatch(file_name, NAME_PATTERN)


def url_file_name(url):
    """returns the url's file name"""
    return url[url.rfind('/') + 1:]


def logout(session):
    """Logout from the website"""
    response = session.get(LOGOUT_URL)
    response.raise_for_status()


def main():
    session = requests.session()
    if REQUIRES_AUTHORIZATION:
        login(session)

    os.chdir(TARGET_FOLDER)
    file_count = 0

    for target_url in TARGET_URLS:
        response = session.get(target_url)
        response.raise_for_status()
        page_html = html.fromstring(response.content)
        page_html.make_links_absolute(base_url=target_url)
        for (_, link_type, link_url, _) in page_html.iterlinks():
            if link_type == 'href':
                file_name = url_file_name(link_url)
                if file_name_match(file_name):
                    if not REQUEST_CONFIRMATION or input('Download ' + file_name + ' ? (y/n)') == 'y':
                        file_count = file_count + 1
                        if file_count >= MAX_FILES:
                            break
                        file_name = name_mapping(file_name, str(file_count))
                        print('Downloading as ' + file_name + ' ...')
                        urlrequest.urlretrieve(iri_to_uri(link_url), file_name)

    if REQUIRES_AUTHORIZATION:
        logout(session)

    if file_count == 0:
        print('No files were downloaded.')
    elif file_count == 1:
        print('Finished downloading 1 file!')
    else:
        print('Finished downloading ' + file_count + ' files!')


if __name__ == '__main__':
    main()
