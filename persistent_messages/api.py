from persistent_messages import notify

def add_message(request, level, message, extra_tags='', fail_silently=False, subject='', user=None, email=False, from_user=None, expires=None, close_timeout=None):
    """
    """
    if email:
        notify.email(level, message, extra_tags, subject, user, from_user)
    return request._messages.add(level, message, extra_tags, subject, user, from_user, expires, close_timeout)
