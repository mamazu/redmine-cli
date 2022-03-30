import colorama

color_palette = {
    'status': {
        'New': colorama.Back.BLUE,
        'Resolved': colorama.Back.GREEN + colorama.Fore.BLACK,
        'In Progress': colorama.Back.BLACK,
        'Hold': colorama.Back.RED,
        'Feedback': colorama.Back.YELLOW + colorama.Fore.BLACK,
        'Review': colorama.Back.MAGENTA,
        'QA': colorama.Back.RESET,
    },
    'tracker': {
        'Feature': colorama.Back.GREEN + colorama.Fore.BLACK,
        'Bug': colorama.Back.RED,
        'Support': colorama.Back.YELLOW
    },
    'reset': colorama.Back.RESET + colorama.Fore.RESET
}

naming_conventions = {
    'title':
    lambda issue: issue['subject'],
    'feature':
    lambda issue: f"{issue['tracker']['name'].lower()}-{issue['id']}",
    'b24':
    lambda issue:
    f"{issue['project']['name'].split(' ')[-1].upper()}-{issue['id']}-{issue['subject']}"
}
