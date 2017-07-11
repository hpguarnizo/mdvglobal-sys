def verify_user(user):
    if user.email == None or len(user.email) < 3:
        return False
