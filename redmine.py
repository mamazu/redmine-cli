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
    for p in iterate_response(curry_with_filters(rm.get_projects, args.filters), 'projects'):
        print(p['id'], "|", p['name'], "|", p['description'].strip().replace("\n", "\\n").replace('\r', ''))
elif args.subject == 'issues':
    for idx, i in enumerate(iterate_response(curry_with_filters(rm.get_issues, args.filters), 'issues')):
        description = i['description'].strip().replace("\n", "\\n").replace('\r', '')
        print(i['id'], "|", i['subject'], '|', i['status']['name'], '|', description)
        if idx == 10:
            exit()
elif args.subject == 'users':
    result = rm.get_users()

print_result(result)
