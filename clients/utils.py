import sys

class BadRequest(BaseException):
    def __init__(self, response):
        self.response = response

    def __str__(self):
        return '[{code}] {message}'.format(code=self.response.status_code, message=self.response.content)

def iterate_response(endpoint, data_path, auto_confirm=False):
    try:
        json = endpoint()
        total = json['total_count']
        count = 0
        page = 1
        # return
        while count < total:
            for item in json[data_path]:
                yield item
                count += 1
            page += 1
            if not auto_confirm and not confirm_contine():
                return
            json = endpoint(page=page)
    except KeyboardInterrupt:
        pass

def confirm_contine():
    if not sys.__stdin__.isatty():
        return True

    return input('Continue? [y/n, Default: y]').lower() in ('y', '')

def curry_with_filters(f, filter_args):
    return lambda page=1: f(filter_args=filter_args, page=page)
