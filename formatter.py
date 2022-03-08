class PipeFormatter:
    @staticmethod
    def _print_headline(content):
        print('\033[1m=== {content} ===\033[0m'.format(content=content))

    @staticmethod
    def print_summary(details):
        hidden_properties = ['identifier', 'type']
        print('|'.join([str(v) for k, v in details.items() if k not in hidden_properties]))

    @staticmethod
    def format_project_details(project):
        print('Name: {name} ({id})'.format(name=project['name'], id=project['identifier']))
        print('Parent: {name} ({id})'.format(name=project['parent']['name'], id=project['parent']['id']))
        print('Status: ' + str(project['status']))

    @staticmethod
    def format_issue_details(issue):
        PipeFormatter._print_headline(issue['subject'])
        if issue['description'] == '':
            print('-- No description --')
        else:
            print(issue['description'])
        print()
        print()
        print('Project: {name} ({id})'.format(name=issue['project']['name'], id=issue['project']['id']))
        print('Tracker: {name}'.format(name=issue['tracker']['name']))
        print('Status: {name}'.format(name=issue['status']['name']))
        print('Priority: {name}'.format(name=issue['priority']['name']))
        print('Author: {name}'.format(name=issue['author']['name']))
        print('Assignee: {name}'.format(name=issue['assigned_to']['name']))
        if 'estimated_hours' in issue:
            print('Estimated hours: {name}'.format(name=issue['estimated_hours']))
        print('Spent hours: {name}'.format(name=issue['spent_hours']))
        print()
        print('Comments:')
        for issue_comment in issue['journals']:
            if issue_comment['notes'] == '':
                PipeFormatter._format_details(issue_comment['details'])

            else:
                PipeFormatter._print_headline(issue_comment['user']['name'])
                print(issue_comment['notes'])

    @staticmethod
    def _format_details(details):
        for detail in details:
            detail_type = detail['property']
            key = detail['name']
            value = detail['new_value']
            if detail_type in ['attr', 'relation']:
                if detail_type == 'attr':
                    detail_type = 'attribute'
                print(
                    '\033[1mSetting {type}: {key} = {value}\033[0m'.format(type=detail_type, key=key, value=value)
                )
            else:
                print(detail)

    @staticmethod
    def format_user_details(user):
        print('User: {name} ({id})'.format(name=user['login'], id=user['id']))
        print('Name: {firstName} {lastName}'.format(firstName=user['firstname'], lastName=user['lastname']))
        print('Last login: {lastLogin}'.format(lastLogin=user['last_login_on']))
        print()

        PipeFormatter._print_headline('Memberships')
        for membership in user['memberships']:
            roles = []
            for role in membership['roles']:
                if 'inherited' in role:
                    roles.append('\033[92m{roleName}\033[0m'.format(roleName=role['name']))
                else:
                    roles.append(role['name'])

            print('Project: {name}'.format(name=membership['project']['name']))
            print('Roles: {roles}'.format(roles=' | '.join(roles)))
            print()

    @staticmethod
    def format_time_summary(entry):
        user = entry['user']
        activity = entry['activity']
        project = entry['project']
        issue = None
        if 'issue' in entry:
            issue = entry['issue']['id']


        info = [
            str(entry['id']),
            '{name} ({id})'.format(name=project['name'], id=project['id']),
            str(issue),
            '{name} ({id})'.format(name=user['name'], id=user['id']),
            '{name} ({id})'.format(name=activity['name'], id=activity['id']),
            str(entry['hours']),
            entry['comments'] if entry['comments'] != '' else '---'
        ]
        print('|'.join(info))

class LinkFormatter:
    def __init__(self, client):
        self.client = client

    def print_summary(self, details):
        print(self.client._get_url(details['type'], details['identifier'], ''))

    def format_user_details(self, user):
        print(self.client._get_url('users', user['id'], ''))

    def format_issue_details(self, entry):
        print(self.client._get_url('issues', entry['id'], ''))

    def format_time_summary(self, entry):
        print(self.client._get_url('time_entries', entry['id']))

