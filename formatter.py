from ui import format_status, format_tracker


class PipeFormatter:

    @staticmethod
    def _print_headline(content):
        print('\033[1m=== {content} ===\033[0m'.format(content=content))

    @staticmethod
    def print_summary(details: dict) -> None:
        import colorama

        hidden_properties = ['identifier', 'type']
        string = ""
        for key, value in details.items():
            if key in hidden_properties:
                continue
            if key == 'description':
                string += value[:100]
            elif key == 'status':
                string += format_status(value)
            else:
                string += str(value)
            string += "|"
        print(string.strip("|"))

    @staticmethod
    def format_project_details(project):
        print('Name: {name} ({id})'.format(name=project['name'],
                                           id=project['identifier']))
        print('Parent: {name} ({id})'.format(name=project['parent']['name'],
                                             id=project['parent']['id']))
        print('Status: ' + str(project['status']))

    @staticmethod
    def format_issue_details(issue):
        PipeFormatter._print_headline(issue['subject'])
        print('Id: {name}'.format(name=issue['id']))
        if issue['description'] == '':
            print('-- No description --')
        else:
            print('Description:\n' + issue['description'])
        print()
        print()
        print('Project: {name} ({id})'.format(name=issue['project']['name'],
                                              id=issue['project']['id']))
        print('Tracker: {name}'.format(
            name=format_tracker(issue['tracker']['name'])))
        print('Status: {name}'.format(
            name=format_status(issue['status']['name'])))
        print('Priority: {name}'.format(name=issue['priority']['name']))
        print('Author: {name}'.format(name=issue['author']['name']))
        print('Assignee: {name}'.format(name=issue['assigned_to']['name']))
        if 'estimated_hours' in issue:
            print('Estimated hours: {name}'.format(
                name=issue['estimated_hours']))
        print('Spent hours: {name}'.format(name=issue.get('spent_hours', 0)))
        print()
        print('Comments:')
        for issue_comment in issue.get('journals', []):
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
                print('\033[1mSetting {type}: {key} = {value}\033[0m'.format(
                    type=detail_type, key=key, value=value))
            else:
                print(detail)

    @staticmethod
    def format_user_details(user):
        print('User: {name} ({id})'.format(name=user['login'], id=user['id']))
        print('Name: {firstName} {lastName}'.format(
            firstName=user['firstname'], lastName=user['lastname']))
        print(
            'Last login: {lastLogin}'.format(lastLogin=user['last_login_on']))
        print()

        PipeFormatter._print_headline('Memberships')
        for membership in user['memberships']:
            roles = []
            for role in membership['roles']:
                if 'inherited' in role:
                    roles.append('\033[92m{roleName}\033[0m'.format(
                        roleName=role['name']))
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
            str(entry['id']), '{name} ({id})'.format(name=project['name'],
                                                     id=project['id']),
            str(issue), '{name} ({id})'.format(name=user['name'],
                                               id=user['id']),
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


class AgileFormatter:

    def __init__(self, table_width: int):
        self.table_width = table_width

    def format(self, by_assignee) -> None:
        for name, status_list in by_assignee.items():
            print('\033[1m{content}\033[0m'.format(
                content=(f' {name} ').center(self.table_width, '=')))
            keys = status_list.keys()
            width_per_column = self.table_width // len(keys)
            print('|', end='')
            for current_status in keys:
                print(format_status(current_status.center(width_per_column)) +
                      '|',
                      end='')
            print('\033[0m')

            format_string_for_column = '{0:<' + str(width_per_column) + '}|'
            i = 0
            hasIssues = True
            while hasIssues:
                line_content = '|'
                hasIssues = False
                for key in keys:
                    if i < len(status_list[key]):
                        hasIssues = True
                        issue = status_list[key][i]
                        title = (str(issue['id']) + ': ' +
                                 issue['subject'])[:width_per_column]
                    else:
                        title = ''
                    line_content += format_string_for_column.format(title)
                i += 1
                if hasIssues:
                    print(line_content)
            print()
