# TODO(colin): fix these lint errors (http://pep8.readthedocs.io/en/release-1.7.x/intro.html#error-codes)
# pep8-disable:E128,E302
""" An interactive script for testing Khan Academy API Authentication.
This is an example of how to use the /api/auth2 authentication flow.
See https://github.com/Khan/khan-api/wiki/Khan-Academy-API-Authentication for
documentation.
"""
import inspect
import json
import cgi

import os
import rauth
import http.server
import socketserver
import time
import webbrowser

# You can get a CONSUMER_KEY and CONSUMER_SECRET for your app here:
# http://www.khanacademy.org/api-apps/register
CONSUMER_KEY = 'cJug9HHWWU84Wsjw'
CONSUMER_SECRET = 'YCWpcRHwUMP6Qnsv'

CALLBACK_BASE = '127.0.0.1'
SERVER_URL = 'http://www.khanacademy.org'

DEFAULT_API_RESOURCE = '/api/v1/playlists'
VERIFIER = None
khan_dic = {}

each_info = []
keys = ["description", "keywords", "png", "ka_url", "views"]


# Create the callback server that's used to set the oauth verifier after the
# request token is authorized.
def create_callback_server():
    class CallbackHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            global VERIFIER

            params = cgi.parse_qs(self.path.split('?', 1)[1],
                                  keep_blank_values=False)
            VERIFIER = params['oauth_verifier'][0]

            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write('OAuth request token fetched and authorized;' + ' you can close this window.')

        def log_request(self, code='-', size='-'):
            pass

    server = socketserver.TCPServer((CALLBACK_BASE, 0), CallbackHandler)
    return server


# Make an authenticated API call using the given rauth session.
def get_api_resource(session):
    resource_url =DEFAULT_API_RESOURCE

    url = SERVER_URL + resource_url
    split_url = url.split('?', 1)
    params = {}

    # Separate out the URL's parameters, if applicable.
    if len(split_url) == 2:
        url = split_url[0]
        params = cgi.parse_qs(split_url[1], keep_blank_values=False)

    start = time.time()
    response = session.get(url, params=params)
    #print(response.text)
    end = time.time()

    print("\n")
    #print(response.text)
    responseX = json.loads(response.text)
    print(responseX[0]['title'])
    return response

    '''text_file = open(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) +'/data1.json', 'r')
    cleardic = {}
    for line in response.json():
        each_video = json.loads(line)
        print(each_video)
        title = each_video['title']
        description = each_video['description']
        keywords = each_video['keywords']
        png = each_video['png']
        price = 0
        ka_url = each_video['ka_url']
        views = each_video['views']
        cleardic[title] = {"description": description, "keywords": keywords,
                           "png": png, "price": "0", "ka_url": ka_url,
                           "views": views}

    print(cleardic)'''


def run_tests():
    global CONSUMER_KEY, CONSUMER_SECRET, SERVER_URL

    # Set consumer key, consumer secret, and server base URL from user input or
    # use default values.

    # Create an OAuth1Service using rauth.
    service = rauth.OAuth1Service(
        name='test',
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        request_token_url=SERVER_URL + '/api/auth2/request_token',
        access_token_url=SERVER_URL + '/api/auth2/access_token',
        authorize_url=SERVER_URL + '/api/auth2/authorize',
        base_url=SERVER_URL + '/api/auth2')

    callback_server = create_callback_server()

    # 1. Get a request token.
    request_token, secret_request_token = service.get_request_token(
        params={'oauth_callback': 'http://%s:%d/' %
                                  (CALLBACK_BASE, callback_server.server_address[1])})

    # 2. Authorize your request token.
    authorize_url = service.get_authorize_url(request_token)
    webbrowser.open(authorize_url)

    callback_server.handle_request()
    callback_server.server_close()

    # 3. Get an access token.
    session = service.get_auth_session(request_token, secret_request_token,
                                       params={'oauth_verifier': VERIFIER})

    # Repeatedly prompt user for a resource and make authenticated API calls.
    print()
    get_api_resource(session)


def main():
    run_tests()


if __name__ == "__main__":
    main()
