from requests import get, post
from base64 import b64encode
from json.decoder import JSONDecodeError

class BadRequest(BaseException):
    def __init__(self, response):
        self.response = response

class RedmineClient:
    def __init__(self, username, password, base_url):
        pass_string = username + ':' + password
        self.authorization = 'Basic ' + b64encode(pass_string.encode('utf-8')).decode('utf-8')
        self.base_url = base_url
        self.limit = 100

    def _to_json(self, url, page=1):
        url= self.base_url + url
        r = get(url=url, headers={'Authorization': self.authorization}, params={'page': page, 'limit': self.limit})
        if r.status_code >= 400:
            raise BaseException(r)
        return r.json()
    
    def get_projects(self, page=1):
        return self._to_json('/projects.json')
    
    def get_issues(self, page, filter={}):
        return self._to_json('/issues.json')
    
    def get_users(self):
        return self._to_json('/users.json')

def iterate_response(endpoint):
    json = endpoint()
    total = json['total_count']
    count = 0
    page = 1

    while count < total:
        for item in json['projects']:
            yield item
            count += 1
        page += 1
        json = endpoint(page=page)
