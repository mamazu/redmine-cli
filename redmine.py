#!/usr/bin/env python3
import sys

from credentials import get_credentials
from clients.utils import iterate_response, BadRequest, curry_with_filters
from clients.clients import ProjectClient, IssueClient, UserClient, TimeEntryClient
from formatter import PipeFormatter, LinkFormatter

formatter = PipeFormatter()
[url, username, password] = get_credentials()

def handle_time_args(args) -> None:
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
                sys.exit(1)
            return
        else:
            time_entries = rm.get_time_entries(filter_args={'issue_id': args.id})['time_entries']
    else:
        filter_params = {"user_id": "me"}
        time_entries = iterate_response(
            curry_with_filters(rm.get_time_entries, filter_params),
            'time_entries'
        )
    count = 0
    for entry in time_entries:
        formatter.format_time_summary(entry)
        count += 1

    if count == 0:
        print('No time entries with the current selection')

def handle_users(args):
    rm = UserClient(username, password, url)
    if args.me:
        item = rm.get_current_user()
        formatter.format_user_details(item['user'])
    elif args.id is not None:
        item = rm.get_user(args.id)
        formatter.format_user_details(item['user'])
    else:
        print(rm.get_users())

def handle_projects(args):
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

def handle_issues(args) -> None:
    rm = IssueClient(username, password, url)
    global formatter
    if args.format == 'link':
        formatter = LinkFormatter(rm)
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


def parse_args():
    from argparse import ArgumentParser

    parser = ArgumentParser()
    subparsers = parser.add_subparsers()

    time_parser = subparsers.add_parser('time', help="Manage the time spend on a ticket")
    time_parser.add_argument('--time', default=None, required=False, help='Enters a time into the given issue', type=float)
    time_parser.add_argument('--comment', default='', required=False, help='Comment for a time entry')
    time_parser.add_argument('--id', default=None, required=False, help='Id of the issue')
    time_parser.set_defaults(func=handle_time_args)

    user_parser = subparsers.add_parser('user', help="User management (currently not fully implemented)")
    user_parser.add_argument('--id', default=None, required=False, help='Id of the issue / project for detailed info')
    user_parser.add_argument('--format', default='|', choices=['|', 'link'], required=False)
    user_parser.add_argument('--me', default=False, action='store_true', required=False,
                        help='Ones visible or assigned to me')
    user_parser.set_defaults(func=handle_users)

    issues_parser = subparsers.add_parser('issues', help="Listing and managing issues")
    issues_parser.add_argument('id', default=None, help='Id of the issue / project for detailed info')
    issues_parser.add_argument('--format', default='|', choices=['|', 'link'], required=False)
    issues_parser.add_argument('--me', default=False, action='store_true', required=False,
                        help='Ones visible or assigned to me')
    issues_parser.set_defaults(subject='issues', func=handle_issues)

    project_parser = subparsers.add_parser('projects', help="Listing projects")
    project_parser.add_argument('--id', default=None, required=False, help='Id of the issue / project for detailed info')
    project_parser.add_argument('--format', default='|', choices=['|', 'link'], required=False)
    project_parser.add_argument('--me', default=False, action='store_true', required=False,
                        help='Ones visible or assigned to me')
    project_parser.set_defaults(subject='projects', func=handle_projects)

    return parser.parse_args()

def parse_filters(arguments):
    filter_params = {}
    if 'subject' in arguments:
        if arguments.subject == 'project' and arguments.me:
            filter_params = {'public': 'false'}
        elif arguments.subject == 'issues' and arguments.me:
            filter_params = {'assigned_to_id': 'me'}

    arguments.filters = filter_params
    return arguments

args = parse_args()
args = parse_filters(args)
args.func(args)
