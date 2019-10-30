from client import RedmineClient

class Formatter:
    def __init__(self, format):
        self.format = format

    def print_summary(self, client, details):
        hidden_properties = ['identifier', 'type']
        if self.format == 'link':
            print(RedmineClient._get_url(client, details['type'], details['identifier'], ''))
        else:
            print('|'.join([str(v) for k, v in details.items() if k not in hidden_properties]))

    def format_project_details(self, project):
        print('Name: {name} ({id})'.format(name=project['name'], id=project['identifier']))
        print('Parent: {name} ({id})'.format(name=project['parent']['name'], id=project['parent']['id']))
        print('Status: ' + str(project['status']))

    def format_issue_details(self, issue):
        print('\033[1m==={name}===\033[0m'.format(name=issue['subject'])) 
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
                details = issue_comment['details']
                for detail in details:
                    if detail['property'] == 'attr':
                        print('\033[1mSetting attribute: {attr} = {value}\033[0m'.format(attr=detail['name'], value=detail['new_value']))
                    elif detail['property'] == 'relation':
                        print('\033[1mSetting relation: {relation} = {value}\033[0m'.format(relation=detail['name'], value=detail['new_value']))
                    else:
                        print(detail)
            else:
                print('\033[1m==={name}===\033[0m'.format(name=issue_comment['user']['name']))
                print(issue_comment['notes'])

    def format_user_details(self, user):
        print('User: {name} ({id})'.format(name=user['login'], id=user['id']))
        print('Name: {firstName} {lastName}'.format(firstName=user['firstname'], lastName=user['lastname']))
        print('Last login: {lastLogin}'.format(lastLogin=user['last_login_on']))
        print()
        
        print('\033[1m=== Memberships ===\033[0m') 
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