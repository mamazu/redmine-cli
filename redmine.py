from console import parse_args, parse_filters
from credentials import get_credentials
from clients.utils import iterate_response, BadRequest, curry_with_filters
from clients.clients import ProjectClient, IssueClient, UserClient, TimeEntryClient
from formatter import PipeFormatter, LinkFormatter

[url, username, password] = get_credentials()

args = parse_args()
args = parse_filters(args)

formatter = PipeFormatter()

if args.subject == 'projects':
    rm = ProjectClient(username, password, url)
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
            formatter.print_summary(summary)
elif args.subject == 'issues':
    rm = IssueClient(username, password, url)
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
            formatter.print_summary(summary)
elif args.subject == 'users':
    rm = UserClient(username, password, url)
    if args.me:
        item = rm.get_current_user()
        formatter.format_user_details(item['user'])
    elif args.id is not None:
        item = rm.get_user(args.id)
        formatter.format_user_details(item['user'])
    else:
        print(rm.get_users())
elif args.subject == 'time':
    rm = TimeEntryClient(username, password, url)
    if args.id:
        method = rm.enter_issue_time
        if args.id[0] == 'p':
            method = rm.enter_project_time
        if args.time:
            try:
                method(args.id, args.time, comment=args.comment)
            except BadRequest as b:
                print(b)
            time_entries = []
        else:
            time_entries = rm.get_time_entries(filter_args={'issue_id': args.id})['time_entries']
    else:
        time_entries = iterate_response(
            curry_with_filters(rm.get_time_entries, args.filters),
            'time_entries'
        )
    for entry in time_entries:
        print(entry)
        formatter.format_time_summary(entry)
