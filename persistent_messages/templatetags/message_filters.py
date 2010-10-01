# coding=utf-8
from django import template  
 
def latest(queryset, count):
    return queryset.order_by('-created')[:count]

def latest_or_unread(queryset, count):
    count_unread = queryset.filter(read=False).count()
    if count_unread > count:
        count = count_unread
    return queryset.order_by('read', '-created')[:count]
    
register = template.Library()  
register.filter(latest)  
register.filter(latest_or_unread)