# remine-cli
A cli programm to manage redmine tickets.

## How to run
You can run the program `redmine.py` and when running it the first time it will ask you for the hostname and your credentials.

Commands:

| Command | Description |
|-----|-----|
| redmine.py projects | Returns a list of all projects |
| redmine.py issues | Returns a list of all issues |
| redmine.py time | Get time data into redmine|

### Entering data into the system
Enter time entries:
* `python3 redmine.py time --id <issue_id> --time <time>`