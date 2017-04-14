import hashlib


class RegisterTokenGenerator(object):
    _salt = "accounts.tokens.RegisterTokenGenerator"

    def make_token(self, user):
        control_string = "{salt}{user_id}{user_name}".format(
            salt=self._salt, user_id=user.id,
            user_name=user.username
        ).encode()

        return hashlib.md5(control_string).hexdigest()

    def make_token_from_date_joined(self, user):
        control_string = "{salt}{user_id}{user_date_joined}".format(
            salt=self._salt, user_id=user.id,
            user_date_joined=user.date_joined.strftime("%Y%m%d%H%M%S")
        ).encode()

        return hashlib.md5(control_string).hexdigest()

    def check_token(self, user, token):
        valid_tokens = (self.make_token(user),
                        self.make_token_from_date_joined(user))

        if token in valid_tokens:
            return True

        return False
