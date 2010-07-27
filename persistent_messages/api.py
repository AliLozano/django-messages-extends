def add_message(request, level, message, extra_tags='', fail_silently=False, subject='', user=None, email=False, from_user=None):
    """
    """
    if email:
        from persistent_messages import notify
        notify.email(level, message, extra_tags, subject, user, from_user)
    return request._messages.add(level, message, extra_tags, subject, user, from_user)
