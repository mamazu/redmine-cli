from console import parse_args, print_result, parse_filters
from credentials import get_credentials
from client import iterate_response
from client import RedmineClient

[url, username, password] = get_credentials()
rm = RedmineClient(username, password, url)

args = parse_args()
args = parse_filters(args)


def curry_with_filters(f, filter_args):
    return lambda page=1: f(filter_args=filter_args, page=page)


result = None
if args.subject == 'projects':
    if args.id is not None:
        item = rm.get_project_details(args.id)
        project = item['project']
        print('Name: {name} ({id})'.format(name=project['name'], id=project['identifier']))
        print('Parent: {name} ({id})'.format(name=project['parent']['name'], id=project['parent']['id']))
        print('Status: ' + str(project['status']))
    else:
        for p in iterate_response(curry_with_filters(rm.get_projects, args.filters), 'projects'):
            print(p['id'], "|", p['name'], "|", p['description'].strip().replace("\n", "\\n").replace('\r', ''))
elif args.subject == 'issues':
    if args.id is not None:
        item = rm.get_issue(args.id)
        issue = item['issue']
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
    else:
        for item in iterate_response(curry_with_filters(rm.get_issues, args.filters), 'issues'):
            description = item['description'].strip().replace("\n", "\\n").replace('\r', '')
            print(item['id'], "|", item['subject'], '|', item['status']['name'], '|', description)
elif args.subject == 'users':
    result = rm.get_users()

print_result(result)
