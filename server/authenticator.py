import config


def auth(auth_pass):
    if str(config.authorization).lower() == "true" or config.authorization == True:
        authorization = True
    else:
        authorization = False
    auth_secret = config.auth_secret

    if authorization:
        if auth_pass == auth_secret:
            return True
        else:
            return False
    else:
        return True