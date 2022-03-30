from clients.clients import ProjectClient
from clients.utils import iterate_response
from typing import Dict, Optional
import config

def select_from_list(options: Dict[str, str]) -> Optional[str]:
    while True:
        for key, entry in options:
            print(f"{key}) {entry}")

        try:
            selected_key = input('Selected option: ')
        except KeyboardInterrupt:
            return None

        for key, _ in options:
            if selected_key == str(key):
                return key
        print('Could not find an option for the provided input. Try again!')

def select_project(client: ProjectClient) -> str:
    project_list = dict({
            project['id']: f"{project['name']} - {project['description'][:100]}"
            for a in iterate_response(client.get_projects, 'projects', auto_confirm=True)
        })
    select_from_list(project_list)

def format_status(status: str) -> str:
    color = config.color_palette['status'][status.strip()]
    return color + status + config.color_palette['reset']

def format_tracker(tracker: str) -> str:
    color = config.color_palette['tracker'][tracker.strip()]
    return color + tracker + config.color_palette['reset']

