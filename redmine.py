from credentials import get_credentials
from client import iterate_response
from client import RedmineClient
from argparse import ArgumentParser

[url, username, password] = get_credentials()
rm = RedmineClient(username, password, url)

parser = ArgumentParser()
parser.add_argument('subject', choices=['issues', 'projects', 'users'],
                    help='About what type of subject do you want to get information'
                    )
parser.add_argument('--format', default='|', required=False)
parser.add_argument('--me', default=False, action='store_true', required=False, help='Ones visible or assigned to me')

args = parser.parse_args()
print(args)

if args.subject == 'projects':
    for p in iterate_response(rm.get_projects, 'projects'):
        print(p['id'], "|", p['name'], "|", p['description'].strip().replace("\n", "\\n").replace('\r', ''))
elif args.subject == 'issues':
    for issue in iterate_response(rm.get_issues, 'issues'):
        print(issue)
elif args.subject == 'users':
    for users in rm.get_users():
        print(users)
