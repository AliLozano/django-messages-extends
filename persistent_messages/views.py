from persistent_messages.models import Message
from persistent_messages.storage import get_user
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.core.exceptions import PermissionDenied

def message_detail(request, message_id):
    user = get_user(request)
    if not user.is_authenticated():
        raise PermissionDenied
    message = get_object_or_404(Message, user=user, pk=message_id)
    message.read = True
    message.save()
    return render_to_response('persistent_messages/message/detail.html', {'message': message}, 
        context_instance=RequestContext(request))

def message_mark_read(request, message_id):
    user = get_user(request)
    if not user.is_authenticated():
        raise PermissionDenied
    message = get_object_or_404(Message, user=user, pk=message_id)
    message.read = True
    message.save()
    if not request.is_ajax():
        return HttpResponseRedirect(request.META.get('HTTP_REFERER') or '/')
    else:
        return HttpResponse('')

def message_mark_all_read(request):
    user = get_user(request)
    if not user.is_authenticated():
        raise PermissionDenied
    Message.objects.filter(user=user).update(read=True)
    if not request.is_ajax():
        return HttpResponseRedirect(request.META.get('HTTP_REFERER') or '/')
    else:
        return HttpResponse('')
