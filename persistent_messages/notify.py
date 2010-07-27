from django.core.mail import send_mail

def email(level, message, extra_tags, subject, user, from_user):
    send_mail(subject, message, from_user.email if from_user else None, [user.email], fail_silently=False)
