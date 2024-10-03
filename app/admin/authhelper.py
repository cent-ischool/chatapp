

def get_email(auth_data):
    return auth_data['account']["idTokenClaims"]["preferred_username"]

def get_name(auth_data):
    return auth_data['account']["idTokenClaims"]["name"]

def get_session_id(auth_data):
    return auth_data["account"]["localAccountId"]

