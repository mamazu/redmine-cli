from requests import get, post
from base64 import b64encode
import json
from clients.utils import BadRequest


class RedmineClient:
    def __init__(self, username, password, base_url):
        pass_string = username + ':' + password
        self.authorization = 'Basic ' + b64encode(pass_string.encode('utf-8')).decode('utf-8')
        self.base_url = base_url.rstrip('/')
        self.limit = 100

    def _get_url(self, resource_type, resource_id=None, format_='.json') -> str:
        url = ''
        if resource_id is not None:
            url = '/{id}'.format(id=resource_id)
        return self.base_url + '/' + resource_type + url + format_

    def _get_authorization(self):
        return {'Authorization': self.authorization}

    def _to_json(self, url, filter_args=None, page=1) -> dict:
        if type(filter_args) is not dict:
            filter_args = {}
        filter_args['page'] = page
        filter_args['limit'] = self.limit

        r = get(url=url, headers=self._get_authorization(), params=filter_args)
        if r.status_code >= 400:
            print(url)
            raise BadRequest(r)
        return r.json()


class ProjectClient(RedmineClient):
    def get_projects(self, *, filter_args=None, page=1) -> dict:
        return self._to_json(self._get_url('projects'), filter_args, page)

    def get_project_details(self, project_id) -> dict:
        return self._to_json(self._get_url('projects', project_id))


class IssueClient(RedmineClient):
    def get_issue(self, issue_id) -> dict:
        return self._to_json(self._get_url('issues', issue_id), {'include': 'journals'})

    def get_issues(self, *, page=1, filter_args=None) -> dict:
        return self._to_json(self._get_url('issues'), filter_args, page)

    def create_issue(self, project_id: int, title: str, description: str) -> dict:
        params = {
            'issue': {
                'project_id': project_id,
                'subject': title,
                'description': description
             }
        }
        url = self._get_url('issues')
        json_data = json.dumps(params)

        headers = self._get_authorization()
        headers['content-type'] = 'application/json'

        r = post(url, headers=headers, data=json_data)
        if r.status_code >= 400:
            raise BadRequest(r)
        return r.json()


class UserClient(RedmineClient):
    def get_user(self, user_id) -> dict:
        return self._to_json(self._get_url('users', user_id), {"include": "memberships"})

    def get_current_user(self) -> dict:
        return self._to_json(self._get_url('users', 'current'), {"include": 'memberships'})

    def get_users(self) -> dict:
        return self._to_json(self._get_url('users'))


class TimeEntryClient(RedmineClient):
    def get_time_entries(self, filter_args=None, page=1) -> dict:
        return self._to_json(self._get_url('time_entries'), filter_args, page)

    def get_time_entry_activities(self) -> dict:
        formatted_activities = {}
        activities = self._to_json(self.base_url + '/enumerations/time_entry_activities.json')['time_entry_activities']
        for activity in activities:
            formatted_activities[activity['name']] = activity['id']

        return formatted_activities

    def _get_time_entry_date(self, key, id, time, entry_date, activity=None, comment=''):
        activities = self.get_time_entry_activities()
        if activity in activities:
            activity_id = activities[activity]
        else:
            activity_id = list(activities.values())[0]
            activity = list(activities.keys())[0]

        params = {
            key: id,
            'hours': time,
            'activity_id': activity_id,
            'comments': comment if comment != '' else activity,
        }

        if entry_date is not None:
            params['spent_on'] = entry_date
        return {'time_entry': params}

    def _post_entry_time(self, params):
        url = self.base_url + '/time_entries.json'
        json_data = json.dumps(params)

        headers = self._get_authorization()
        headers['content-type'] = 'application/json'

        r = post(url, headers=headers, data=json_data)
        if r.status_code >= 400:
            raise BadRequest(r)

    def enter_project_time(self, project_id, time, entry_date=None, comment=""):
        project_id = project_id[1:]
        params = self._get_time_entry_date('project_id', project_id, time, entry_date, comment=comment)
        self._post_entry_time(params)

    def enter_issue_time(self, issue_id, time, entry_date=None, comment=""):
        params = self._get_time_entry_date('issue_id', issue_id, time, entry_date, comment=comment)
        self._post_entry_time(params)
