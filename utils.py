from html import escape

class TemplateDict(dict):
    def __init__(self, escape=True, **kwargs):
        if escape:
            safe_data = {k: self._escape(v) for k, v in kwargs.items()}
        else:
            safe_data = kwargs
        super().__init__(safe_data)
    
    def _escape(self, value):
        if isinstance(value, str):
            return escape(value)
        return value
    
    def __missing__(self, key):
        return f'{{{key}}}'


def read_file(filename):
    with open(filename, 'r') as f:
        content = f.read()
    return content