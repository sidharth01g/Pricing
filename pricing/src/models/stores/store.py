class Store(object):

    def __init__(self, name: str, url_prefix: str) -> None:
        self.name = name
        self.url_prefix = url_prefix

    def __repr__(self) -> str:
        return '<Store "{}" with URL prefix "{}">'.format(self.name, self.url_prefix)
