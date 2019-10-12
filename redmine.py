from credentials import get_credentials
from client import iterate_response
from client import RedmineClient

[url, username, password] = get_credentials()
rm = RedmineClient(username, password, url)

# for i, p in enumerate(iterate_response(rm.get_projects, 'projects')):
#     print(p['id'], "|", p['name'], "|",  p['description'].strip().replace("\n", "\\n").replace('\r', ''))

for issue in iterate_response(rm.get_issues, 'issues'):
    print(issue)

# for users in rm.get_users():
#     print(users)