import config

def auth(parameter):
    if str(config.authorization).lower() == "true":
        authorization = True
    else:
        authorization = False
    auth_secret = config.auth_secret

    auth_pass = parameter.auth_pass

    if authorization:
        if auth_pass == auth_secret:
            return True
        else:
            return False
    else:
        return True