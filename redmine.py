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
        print(rm.get_project_details(args.id))
    else:
        for p in iterate_response(curry_with_filters(rm.get_projects, args.filters), 'projects'):
            print(p['id'], "|", p['name'], "|", p['description'].strip().replace("\n", "\\n").replace('\r', ''))
elif args.subject == 'issues':
    if args.id is not None:
        print(rm.get_issue(args.id))
    else:
        for i in iterate_response(curry_with_filters(rm.get_issues, args.filters), 'issues'):
            description = i['description'].strip().replace("\n", "\\n").replace('\r', '')
            print(i['id'], "|", i['subject'], '|', i['status']['name'], '|', description)
elif args.subject == 'users':
    result = rm.get_users()

print_result(result)
