from clients.clients import ProjectClient
from clients.utils import iterate_response
from typing import Dict
import config

def select_from_list(options: Dict[str, str]) -> str:
    if len(options) == 0:
        return ''

    while True:
        for key, entry in options.items():
            print(f"{key}) {entry}")

        selected_key = input('Selected option: ')
        for key, _ in options.items():
            if selected_key == key:
                return key
        print('Could not find an option for the provided input. Try again!')


def select_project(client: ProjectClient) -> int:
    project_list = dict({
        str(project['id']):
        f"{project['name']} - {project['description'][:100]}"
        for project in iterate_response(
            client.get_projects, 'projects', auto_confirm=True)
    })
    return int(select_from_list(project_list))


def format_status(status: str) -> str:
    color = config.color_palette['status'][status.strip()]
    return color + status + config.color_palette['reset']


def format_tracker(tracker: str) -> str:
    color = config.color_palette['tracker'][tracker.strip()]
    return color + tracker + config.color_palette['reset']
