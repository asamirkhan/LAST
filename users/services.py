def save_user_type(data, user):
    user_type = data.get('user_type')
    if user_type == 'reviewer':
        user.is_reviewer = True
        user.is_accepted = False
    if user_type == 'reader':
        user.is_reader = True
    user.save()