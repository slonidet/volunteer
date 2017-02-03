import hashlib


class RegisterTokenGenerator(object):
    _salt = "accounts.tokens.RegisterTokenGenerator"

    def make_token(self, user):
        control_string = "{salt}{user_id}{user_date_joined}".format(
            salt=self._salt, user_id=user.id,
            user_date_joined=user.date_joined.strftime("%Y%m%d%H%M%S")
        ).encode()

        return hashlib.md5(control_string).hexdigest()

    def check_token(self, user, token):
        if token == self.make_token(user):
            return True

        return False
