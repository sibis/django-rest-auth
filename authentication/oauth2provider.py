import requests


class Oauth2Provider(object):
    def __init__(self, provider, access_token):
        self.provider = provider
        self.access_token = access_token

    def google_auth(self):
        auth_header = {"Authorization": "OAuth %s" % self.access_token}
        google_auth_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        r = requests.get(google_auth_url,
                         headers=auth_header)
        return r

    def facebook_auth(self):
        fb_url = 'https://graph.facebook.com/me?fields=name,email&access_token=' + self.access_token
        r = requests.get(fb_url)
        return r

    def get_user_details(self):
        oauth_providers = {"google": self.google_auth, "facebook": self.facebook_auth}
        return oauth_providers[self.provider]()
