from console import parse_args, parse_filters
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

formatter = Formatter(args.format)

if args.subject == 'projects':
    if args.id is not None:
        item = rm.get_project_details(args.id)
        formatter.format_project_details(item['project'])
    else:
        for p in iterate_response(curry_with_filters(rm.get_projects, args.filters), 'projects'):
            summary = {
                "type": "projects",
                "identifier": p['identifier'],
                "id": p['id'],
                "name": p['name'],
                "description": p['description'].strip().replace("\n", "\\n").replace('\r', '')
            }
            formatter.print_summary(rm, summary)
elif args.subject == 'issues':
    if args.id is not None:
        item = rm.get_issue(args.id)
        formatter.format_issue_details(item['issue'])
    else:
        for item in iterate_response(curry_with_filters(rm.get_issues, args.filters), 'issues'):
            description = item['description'].strip().replace("\n", "\\n").replace('\r', '')
            summary = {
                "type": "issues",
                "id": item['id'],
                "identifier": item['id'],
                "subject": item['subject'],
                "status": item['status']['name'],
                "description": description
            }
            formatter.print_summary(rm, summary)
elif args.subject == 'users':
    if args.me:
        item = rm.get_current_user()
        formatter.format_user_details(item['user'])
    elif args.id is not None:
        item = rm.get_user(args.id)
        formatter.format_user_details(item['user'])
    else:
        print(rm.get_users())

