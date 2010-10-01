Django Persistent Messages
==========================

A Django app for unified and persistent user messages/notifications, built on top of Django's [messages framework](http://docs.djangoproject.com/en/dev/ref/contrib/messages/) (`django.contrib.messages`).

This app provides support for messages that are supposed to be persistent, that is, they outlast a browser session and will be displayed as “sticky” notes to the user, until they are actively marked as read. Once read, messages are still listed in the message inbox for each user. In short: While `django.contrib.messages` makes sure that messages you create are displayed to the user, this app makes sure that they actually get noticed.  

* For authenticated users, messages are stored in the database. They can be temporary just like regular messages, or persistent as described above.
* For anonymous users, the default cookie/session-based approach is used, i.e. there is no database access for storing messages.
* There is a unified API for displaying messages to both types of users, that is, you can use the same code you'd be using with Django's messaging framework in order to add and display messages, but there is additional functionality available if the user is authenticated.
* Messages can be displayed on-screen and/or sent to individual users as email notifications.

Installation
------------

This document assumes that you are familiar with Python and Django.

1. [Download and unzip the app](http://github.com/philomat/django-persistent-messages/), or clone the source using `git`:

        $ git clone git://github.com/philomat/django-persistent-messages.git

2. Make sure `persistent_messages` is on your `PYTHONPATH`.
3. Add `persistent_messages` to your `INSTALLED_APPS` setting.

        INSTALLED_APPS = (
            ...
            'persistent_messages',
        )

4. Make sure Django's `MessageMiddleware` is in your `MIDDLEWARE_CLASSES` setting (which is the case by default):

        MIDDLEWARE_CLASSES = (
            ...
            'django.contrib.messages.middleware.MessageMiddleware',
        )
 
5. Add the persistent_messages URLs to your URL conf. For instance, in order to make messages available under `http://domain.com/messages/`, add the following line to `urls.py`.

        urlpatterns = patterns('',
            (r'^messages/', include('persistent_messages.urls')),
            ...
        )

6. In your settings, set the message [storage backend](http://docs.djangoproject.com/en/dev/ref/contrib/messages/#message-storage-backends) to `persistent_messages.storage.PersistentMessageStorage`:

        MESSAGE_STORAGE = 'persistent_messages.storage.PersistentMessageStorage'

7. Set up the database tables using 

	    $ manage.py syncdb

8. If you want to use the bundled templates, add the `templates` directory to your `TEMPLATE_DIRS` setting:

        TEMPLATE_DIRS = (
            ...
            'path/to/persistent_messages/templates')
        )


Using messages in views and templates
-------------------------------------

### Message levels ###

Django's messages framework provides a number of [message levels](http://docs.djangoproject.com/en/dev/ref/contrib/messages/#message-levels) for various purposes such as success messages, warnings etc. This app provides constants with the same names, the difference being that messages with these levels are going to be persistent:

    import persistent_messages
    # persistent message levels:
    persistent_messages.INFO 
    persistent_messages.SUCCESS 
    persistent_messages.WARNING
    persistent_messages.ERROR

    from django.contrib import messages
    # temporary message levels:
    messages.INFO 
    messages.SUCCESS 
    messages.WARNING
    messages.ERROR

### Adding a message ###

Since the app is implemented as a [storage backend](http://docs.djangoproject.com/en/dev/ref/contrib/messages/#message-storage-backends) for Django's [messages framework](http://docs.djangoproject.com/en/dev/ref/contrib/messages/), you can still use the regular Django API to add a message:

    from django.contrib import messages
    messages.add_message(request, messages.INFO, 'Hello world.')

This is compatible and equivalent to using the API provided by `persistent_messages`:

    import persistent_messages
    from django.contrib import messages
    persistent_messages.add_message(request, messages.INFO, 'Hello world.')

In order to add a persistent message, use the message levels listed above:

    messages.add_message(request, persistent_messages.WARNING, 'You are going to see this message until you mark it as read.')

or the equivalent:

    persistent_messages.add_message(request, persistent_messages.WARNING, 'You are going to see this message until you mark it as read.')
    
Note that this is only possible for logged-in users, so you are probably going to have make sure that the current user is not anonymous using `request.user.is_authenticated()`. Adding a persistent message for anonymous users raises a `NotImplementedError`.

Using `persistent_messages.add_message`, you can also add a subject line to the message. This makes sense when you are using the email notification feature. The following message will be displayed on-screen and sent to the email address associated with the current user:

    persistent_messages.add_message(request, persistent_messages.INFO, 'Message body', subject='Please read me', email=True)

You can also pass this function a `User` object if the message is supposed to be sent to a user other than the one who is currently authenticated. User Sally will see this message the next time she logs in:

    from django.contrib.auth.models import User
    sally = User.objects.get(username='Sally')
    persistent_messages.add_message(request, persistent_messages.SUCCESS, 'Hi Sally, here is a message to you.', subject='Success message', user=sally)

### Displaying messages ###

Messages can be displayed [as described in the Django manual](http://docs.djangoproject.com/en/dev/ref/contrib/messages/#displaying-messages). However, you are probably going to want to include links tags for closing each message (i.e. marking it as read). In your template, use something like:

    {% if messages %}
    <ul class="messages">
        {% for message in messages %}
        <li{% if message.tags %} class="{{ message.tags }}"{% endif %}>
            {% if message.subject %}<strong>{{ message.subject }}</strong><br />{% endif %}
            {{ message.message }}<br />
            {% if message.is_persistent %}<a href="{% url message_mark_read message.pk %}">close</a>{% endif %}
        </li>
        {% endfor %}
    </ul>
    {% endif %}

You can also use the bundled templates instead. The following line replaces the code above. It allows the user to remove messages and mark them as read using Ajax requests, provided your HTML page includes JQuery:

    {% include "persistent_messages/message/includes/messages.jquery.html" %}
