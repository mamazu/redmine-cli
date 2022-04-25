from ui import format_status, format_tracker


class PipeFormatter:

    @staticmethod
    def _print_headline(content):
        print('\033[1m=== {content} ===\033[0m'.format(content=content))

    @staticmethod
    def print_summary(details: dict) -> None:
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
        print(string.rstrip("|"))

    @staticmethod
    def format_project_details(project):
        parent_project = project['parent']
        print(f"Name: {parent_project['name']} ({parent_project['id']})\nStatus: {project['status']}")

    @staticmethod
    def format_issue_details(issue):
        PipeFormatter._print_headline(issue['subject'])
        if issue['description'] == '':
            issue['description'] = '-- No description --'
        print(f"""
Id: {issue['id']}
Description: {issue['description']}


Project: {issue['project']['name']} ({issue['project']['id']})
Tracker: {issue['tracker']['name']}
Status: {format_status(issue['status']['name'])}

Priority: {issue['priority']['name']}
Author: {issue['author']['name']}
Assignee: {issue['assigned_to']['name']}
        """)
        if 'estimated_hours' in issue:
            print(f"Estimated hours: {issue['estimated_hours']}")

        print(f"Spent hours: {issue.get('spent_hours', 0)}\nComments:")
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
        print(f"User: {user['login']} ({user['id']})")
        print(f"Name: {user['firstname']} {user['lastname']}")
        print(f"Last login: {user['last_login_on']}")
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

            print(f"Project: {membership['project']['name']}")
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
        comment = entry['comments'] if entry['comments'] != '' else '---'

        info = [
            str(entry['id']),
            f'{project["name"]} ({project["id"]})',
            str(issue),
            f'{user["name"]} ({user["id"]})',
            f'{activity["name"]} ({activity["id"]})',
            str(entry['hours']),
            comment
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
