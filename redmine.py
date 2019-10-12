from credentials import get_credentials
from client import iterate_response
from client import RedmineClient

[url, username, password] = get_credentials()
rm = RedmineClient(username, password, url)

# for i, p in enumerate(iterate_response(rm.get_projects)):
#     print(p['id'], "|", p['name'], "|",  p['description'].strip().replace("\n", "\\n").replace('\r', ''))

# for issue in rm.get_issues(page=1,filter={})['issues']:
#     print(issue)

for users in rm.get_users():
    print(users)