class User(object):

    def __init__(self, email: str, password: str) -> None:
        self.email = email
        self.password = password

    def __repr__(self) -> str:
        return '<User with email ID "{}">'.format(self.email)
