from requests import get, post
from base64 import b64encode


class BadRequest(BaseException):
    def __init__(self, response):
        self.response = response


class RedmineClient:
    def __init__(self, username, password, base_url):
        pass_string = username + ':' + password
        self.authorization = 'Basic ' + b64encode(pass_string.encode('utf-8')).decode('utf-8')
        self.base_url = base_url
        self.limit = 100

    def _to_json(self, url, filter_args=None, page=1) -> dict:
        if type(filter_args) is not dict:
            filter_args = {}
        filter_args['page'] = page
        filter_args['limit'] = self.limit

        url = self.base_url + url
        r = get(url=url, headers={'Authorization': self.authorization}, params=filter_args)
        if r.status_code >= 400:
            raise BaseException(r)
        return r.json()

    def get_projects(self, *, filter_args=None, page=1) -> dict:
        return self._to_json('/projects.json', filter_args, page)

    def get_project_details(self, project_id) -> dict:
        return self._to_json('/projects/{id}.json'.format(id=project_id))
    
    def get_issue(self, issue_id) -> dict:
        return self._to_json('/issues/{id}.json'.format(id=issue_id))

    def get_issues(self, *, filter_args=None, page=1) -> dict:
        return self._to_json('/issues.json', filter_args, page)

    def get_users(self) -> dict:
        return self._to_json('/users.json')


def iterate_response(endpoint, data_path):
    json = endpoint()
    total = json['total_count']
    count = 0
    page = 1
    # return
    while count < total:
        for item in json[data_path]:
            yield item
            count += 1
        page += 1
        json = endpoint(page=page)
