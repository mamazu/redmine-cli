import unittest
from unittest import mock
from unittest.mock import MagicMock, call

from formatter import PipeFormatter

class PipeFormatterTest(unittest.TestCase):
    @mock.patch('builtins.print')
    def test_formatting_summary(self, print_mock: MagicMock):
        ticket = {
                "id": 123,
                'status': 'New',
                "name": "Some ticket",
                "description": "This is a ticket with a super long description that should be cut off after 100 characters, testing the timing of the description field in the summary output.",
                'identifier': 'hidden'
            }
        PipeFormatter.print_summary(ticket)
        self.assertEqual(print_mock.call_count, 1)
        print_mock.assert_called_once_with('123|\x1b[44mNew\x1b[49m\x1b[39m|Some ticket|This is a ticket with a super long description that should be cut off after 100 characters, testing ')

    @mock.patch('builtins.print')
    def test_formatting_project_details(self, print_mock: MagicMock):
        project = {
                "parent": {'name': "Project", 'id': 123},
                "status": "Open"
            }
        PipeFormatter.format_project_details(project)
        print_mock.assert_called_once_with('Name: Project (123)\nStatus: Open')

    @mock.patch('builtins.print')
    def test_format_issue_details(self, print_mock: MagicMock):
        issue = {
                "id": 10,
                'subject': "Write tests",
                "description": "",
                "project": {"name": "Main Project", "id": 1 },
                "tracker": {"name": "Bug", "id": 10 },
                "status": {"name": "New", "id": 5},
                "priority": {"name": "High", "id": 1},
                "author": {"name": "Mamamzu", "id": 1},
                "assigned_to": {"name": "Mamamzu", "id": 1},

                }

        PipeFormatter.format_issue_details(issue)

        print_mock.assert_has_calls([
            call('\x1b[1m=== Write tests ===\x1b[0m'),
            call('\nId: 10\nDescription: -- No description --\n\n\nProject: Main Project (1)\nTracker: Bug\nStatus: \x1b[44mNew\x1b[49m\x1b[39m\n\nPriority: High\nAuthor: Mamamzu\nAssignee: Mamamzu\n        '),
            call('Spent hours: 0\nComments:')
            ])

    @mock.patch('builtins.print')
    def test_format_issue_details_with_journal(self, print_mock: MagicMock):
        issue = {
                "id": 10,
                'subject': "Write tests",
                "description": "",
                "project": {"name": "Main Project", "id": 1 },
                "tracker": {"name": "Bug", "id": 10 },
                "status": {"name": "New", "id": 5},
                "priority": {"name": "High", "id": 1},
                "author": {"name": "Mamamzu", "id": 1},
                "assigned_to": {"name": "Mamamzu", "id": 1},
                "journals": [
                    {"notes": "", "details": [
                        {"property": "", "name":"", "new_value":"Testing 123"},
                    ]},
                    {"notes": "This is a note", "user": {"name": "Note heading", "id": 10}}
                ]
            }

        PipeFormatter.format_issue_details(issue)

        print_mock.assert_has_calls([
            call('\x1b[1m=== Write tests ===\x1b[0m'),
            call('\nId: 10\nDescription: -- No description --\n\n\nProject: Main Project (1)\nTracker: Bug\nStatus: \x1b[44mNew\x1b[49m\x1b[39m\n\nPriority: High\nAuthor: Mamamzu\nAssignee: Mamamzu\n        '),
            call('Spent hours: 0\nComments:'),
            call({'property': '', 'name': '', 'new_value': 'Testing 123'}),
            call("\x1b[1m=== Note heading ===\x1b[0m"),
            call('This is a note')
            ])

    @mock.patch('builtins.print')
    def test_format_user_details(self, print_mock: MagicMock):
        user = {
                "id": 10,
                "login": "mamazu",
                "firstname": "John",
                "lastname": "Doe",
                "last_login_on": "2021-10-12 10:00:00",
                "memberships": [],
                }

        PipeFormatter.format_user_details(user)

        print_mock.assert_has_calls([
            call('User: mamazu (10)'),
            call('Name: John Doe'),
            call('Last login: 2021-10-12 10:00:00'),
            call(),
            call('\x1b[1m=== Memberships ===\x1b[0m')
        ])

    @mock.patch('builtins.print')
    def test_format_time_summary(self, print_mock: MagicMock):
        time_entry = {
                "id": 1,
                "user": {"name": "Mamamzu", "id": 10},
                "project": {"name": "Main Project", "id": 1},
                "activity": {"name": "Developing", "id": 5 },
                "comments": "Reading up on how to write tests",
                "hours": 1.5
                }

        PipeFormatter.format_time_summary(time_entry)

        print_mock.assert_has_calls([
            call('1|Main Project (1)|None|Mamamzu (10)|Developing (5)|1.5|Reading up on how to write tests'),
        ])

if __name__ == '__main__':
    unittest.main()
