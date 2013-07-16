import json, hashlib, requests


LASTFM_API_ENDPOINT = 'http://ws.audioscrobbler.com/2.0/'

class LastFmApiException(Exception):
    '''A blank exception specific to LastFmApi.'''


class LastFmApi(object):
    '''An interface to the Last.fm api.

    This class dynamically resolves methods and their parameters. For instance,
    if you would like to access the album.getInfo method, you simply call
    album_getInfo on an instance of LastFmApi.
    '''

    def __init__(self, key, secret):
        self.__api_key = key
        self.__api_secret = secret

    def __getattr__(self, name):
        if name.startswith('__'):
            raise AttributeError()

        def generic_request(*args, **kwargs):
            params = dict(kwargs)
            params['method'] = name.replace('_', '.')
            return self.__send(params)

        generic_request.__name__ = name
        return generic_request

    def __send(self, params):
        params['api_key'] = self.__api_key
        params['format'] = 'json'

        headers = {
            'User-Agent:': 'lastfmapi',
        }

        if (params.has_key('sk') or params['method'] == 'auth.getSession' or params['method'] == 'auth.getToken'):
            params['api_sig'] = self.__sign(params)
            response = requests.post(LASTFM_API_ENDPOINT, params=params, headers=headers).content
        else:
            response = requests.get(LASTFM_API_ENDPOINT, params=params, headers=headers).content


        s = json.loads(response)
        if s.has_key('error'):
            raise LastFmApiException(s['message'])
        return s

    def __sign(self, params):
        keys = list(params.keys())
        keys = filter(lambda x: x != 'format' and x!= 'callback', keys)
        keys.sort()

        string = ""

        for name in keys:
            string += name
            string += params[name]

        string += self.__api_secret
        if type(string) != unicode:
            string = unicode(string, "utf-8")
        string = string.encode("utf-8")
        h = hashlib.md5()
        h.update(string)
        return h.hexdigest()
