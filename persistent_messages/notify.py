from django.core.mail import send_mail

def email(level, message, extra_tags, subject, user, from_user):
    if not user or not user.email:
        raise Exception('Function needs to be passed a `User` object with valid email address.')
    send_mail(subject, message, from_user.email if from_user else None, [user.email], fail_silently=False)
