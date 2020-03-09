# -*- coding: utf-8 -*-
"""views.py: messages extends"""

from messages_extends.models import Message
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied


def callable_or_bool(fn):
    if callable(fn):
        return fn()
    return fn


def message_mark_read(request, message_id):
    if not callable_or_bool(request.user.is_authenticated):
        raise PermissionDenied
    message = get_object_or_404(Message, user=request.user, pk=message_id)
    message.read = True
    message.save()
    if not request.is_ajax():
        return HttpResponseRedirect(request.META.get('HTTP_REFERER') or '/')
    else:
        return HttpResponse('')

def message_mark_all_read(request):
    if not callable_or_bool(request.user.is_authenticated):
        raise PermissionDenied
    Message.objects.filter(user=request.user).update(read=True)
    if not request.is_ajax():
        return HttpResponseRedirect(request.META.get('HTTP_REFERER') or '/')
    else:
        return HttpResponse('')
