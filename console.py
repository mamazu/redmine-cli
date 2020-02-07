def parse_args():
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('subject', choices=['issues', 'projects', 'users', 'time'],
                        help='About what type of subject do you want to get information'
                        )
    parser.add_argument('--id', default=None, required=False, help='Id of the issue / project for detailed info')
    parser.add_argument('--format', default='|', choices=['|', 'link'], required=False)
    parser.add_argument('--me', default=False, action='store_true', required=False,
                        help='Ones visible or assigned to me')
    parser.add_argument('--time', default=None, required=False, help='Enters a time into the given issue', type=float)
    parser.add_argument('--comment', default='', required=False, help='Comment for a time entry')

    return parser.parse_args()


def parse_filters(arguments):
    filter_params = {}
    if arguments.subject == 'project' and arguments.me:
        filter_params = {'public': 'false'}
    elif arguments.subject == 'issues' and arguments.me:
        filter_params = {'assigned_to_id': 'me'}

    arguments.filters = filter_params
    return arguments
