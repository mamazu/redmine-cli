from console import parse_args, print_result, parse_filters
from credentials import get_credentials
from client import iterate_response
from client import RedmineClient
from formatting import Formatter

[url, username, password] = get_credentials()
rm = RedmineClient(username, password, url)

args = parse_args()
args = parse_filters(args)


def curry_with_filters(f, filter_args):
    return lambda page=1: f(filter_args=filter_args, page=page)

formatter = Formatter()

result = None
if args.subject == 'projects':
    if args.id is not None:
        item = rm.get_project_details(args.id)
        formatter.format_project_details(item['project'])
    else:
        for p in iterate_response(curry_with_filters(rm.get_projects, args.filters), 'projects'):
            print(p['id'], "|", p['name'], "|", p['description'].strip().replace("\n", "\\n").replace('\r', ''))
elif args.subject == 'issues':
    if args.id is not None:
        item = rm.get_issue(args.id)
        formatter.format_issue_details(item['issue'])
    else:
        for item in iterate_response(curry_with_filters(rm.get_issues, args.filters), 'issues'):
            description = item['description'].strip().replace("\n", "\\n").replace('\r', '')
            print(item['id'], "|", item['subject'], '|', item['status']['name'], '|', description)
elif args.subject == 'users':
        result = rm.get_users()

print_result(result)
