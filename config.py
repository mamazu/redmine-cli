import colorama
color_palette = {
        'status': {
            'New': colorama.Back.BLUE,
            'Resolved': colorama.Back.GREEN+colorama.Fore.BLACK,
            'In Progress': colorama.Back.BLACK,
            'Hold': colorama.Back.RED,
            'Feedback': colorama.Back.YELLOW+colorama.Fore.BLACK,
            'Review': colorama.Back.MAGENTA,
            'QA': colorama.Back.RESET,
            },
        'tracker': {
            'Feature': colorama.Back.GREEN+colorama.Fore.BLACK,
            'Bug': colorama.Back.RED,
            'Support': colorama.Back.YELLOW
            },

        'reset': colorama.Back.RESET+colorama.Fore.RESET
    }
