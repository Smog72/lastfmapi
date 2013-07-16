LastFmApi
---------

A thin but dynamic wrapper around the Last.fm api webservice found at
http://ws.audioscrobbler.com/2.0/ - You are still required to provide an API key (for read only methods) 
and API secret for write methods (like scrobble)

Installation is easy.

    pip install lastfmapi

Once that's done, you can do something as simple as...

    import lastfmapi
    
    api = lastfmapi.LastFmApi('<your api key here>', None)
    
    api.album_getInfo(artist='Cher', album='Believe')

For methods on the Last.fm api, simply call that method on the api object,
subsituting '_' where '.' would be.

For write methods (like scrobble) you have to do a little more.
First, you have to get SessionKey for your application authorised for selected LastFm user:

    import lastfmapi
    
    api = lastfmapi.LastFmApi('<your api key here>', '<your api secret here>')
    
    TOKEN = api.auth_getToken()[u'token']
    
    print 'Please go to URL below and confirm application authorisation: (use token=' + TOKEN + ') for getSession call\n' +\
              'http://www.last.fm/api/auth/?api_key=' + 'f5ee6af05902fe2eec6e2695e1f69e86' + '&token=' + TOKEN

Once done (user authorised your app's access):

    SESS_KEY = api.auth_getSession(token=TOKEN)['session']['key']
    # you can use it as "sk=" parameter in your WRITE calls to LASTFM.
    
    api.user_shout(user=YouUserName, message='Hello, world!', sk=SESS_KEY)

