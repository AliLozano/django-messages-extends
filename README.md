Django Messages Extends
==========================


[![Build Status](https://travis-ci.org/AliLozano/django-messages-extends.svg?branch=master)](https://travis-ci.org/mpasternak/django-messages-extends)

[![PyPI version](https://badge.fury.io/py/django-messages-extends.svg)](https://badge.fury.io/py/django-messages-extends)


A Django app for extends Django's [messages framework](http://docs.djangoproject
.com/en/dev/ref/contrib/messages/) (`django.contrib.messages`). framework by adding "sticky"  and
 "persistent" backend message storages.  This also supports the notion of sending
 persistent messages to other users in a machine-to-user process.


## Storages ##

### Sticky Storage ###

A "sticky" message is a message where the user must hit the close button in order to get rid of
it within that session.

* For messages that are in some middleware or is only to the current request and don't need save it.
* This is very similar to the default except that you explicitly must close the dialog to remove
the message.
* This backend never save anything only simulate that do that.


### Persistent Storage ###

A "persistent" messages is a message where a message is retained across multiple sessions until
the user clicks the close button.  The message is stored in the default_storage container
(defaults to database).

* Only for authenticated users, messages are stored in the database.
* The messages has to be explicit read, and there are show while don't close it

Installation
------------

This document assumes that you are familiar with Python and Django.

1. [Download and unzip the app](https://github.com/AliLozano/django-messages-extends),
or install using `pip`:

        $ pip install django-messages-extends

2. Make sure `messages_extends` is on your `PYTHONPATH`.
3. Add `messages_extends` to your `INSTALLED_APPS` setting.

```python
INSTALLED_APPS = (
    ...
    'messages_extends',
)
```

4. Make sure Django's `MessageMiddleware` is in your `MIDDLEWARE_CLASSES` setting (which is the
case by default):

```python
MIDDLEWARE_CLASSES = (
    ...
    'django.contrib.messages.middleware.MessageMiddleware',
)
```

5. Add the messages_extends URLs to your URL conf. For instance, in order to make messages
available under `http://domain.com/messages/`, add the following line to `urls.py`.

```python
urlpatterns = patterns('',
    (r'^messages/', include('messages_extends.urls')),
    ...
)
```

6. In your settings, set the message [storage backend](http://docs.djangoproject.com/en/dev/ref/contrib/messages/#message-storage-backends)to `messages_extends.storages.FallbackStorage`:

```python
MESSAGE_STORAGE = 'messages_extends.storages.FallbackStorage'
```

7. Set up the database tables using

	    $ manage.py makemigratations
	    $ manage.py migrate

8. If you want to use the bundled templates, add the `templates` directory to your
`TEMPLATE_DIRS` setting:

```python
TEMPLATE_DIRS = (
    ...
    'path/to/messages_extends/templates')
)
```


Using messages in views and templates
-------------------------------------

### Message levels ###

Django's messages framework provides a number of [message levels](http://docs.djangoproject.com/en/dev/ref/contrib/messages/#message-levels)
for various purposes such as success messages, warnings etc. This app provides constants with the
 same names, the difference being that messages with these levels are going to be persistent:

```python
from messages_extends import constants as constants_messages

# default messages level
constants_messages.DEBUG = 10
constants_messages.INFO = 20
constants_messages.SUCCESS = 25
constants_messages.WARNING = 30
constants_messages.ERROR = 40

# persistent messages level
constants_messages.DEBUG_PERSISTENT = 9
constants_messages.INFO_PERSISTENT = 19
constants_messages.SUCCESS_PERSISTENT = 24
constants_messages.WARNING_PERSISTENT = 29
constants_messages.ERROR_PERSISTENT = 39

# sticky messages level
constants_messages.DEBUG_STICKY = 8
constants_messages.INFO_STICKY = 18
constants_messages.SUCCESS_STICKY = 23
constants_messages.WARNING_STICKY = 28
constants_messages.ERROR_STICKY = 38
```

### Adding a message ###

Since the app is implemented as a [storage backend](http://docs.djangoproject.com/en/dev/ref/contrib/messages/#message-storage-backends)
for Django's [messages framework](http://docs.djangoproject.com/en/dev/ref/contrib/messages/), you
can still use the regular Django API to add a message:

```python
from django.contrib import messages
messages.add_message(request, messages.INFO, 'Hello world.')
```

Or use persistent messages with constants in messages_extends.constants

```python
from django.contrib import messages
from messages_extends import constants as constants_messages
messages.add_message(request, constants_messages.WARNING_PERSISTENT, 'You are going to see this message until you mark it as read.')
```

Or via the shortcut method.

```python
messages.add_persistant_error(request, 'Houston we have a problem..')
```

Note that this is only possible for logged-in users, so you are probably going to have make sure
that the current user is not anonymous using `request.user.is_authenticated()`. Adding a
persistent message for anonymous users raises a `NotImplementedError`.

And sticky messages:

```python
from django.contrib import messages
from messages_extends import constants as constants_messages
messages.add_message(request, constants_messages.WARNING_STICKY, 'You will going to see this messages only in this request')
```

You can also pass this function a `User` object if the message is supposed to be sent to a user
other than the one who is currently authenticated. User Sally will see this message the next time
 she logs in:

```python
from django.contrib import messages
from messages_extends import constants as constants_messages
from django.contrib.auth.models import User
sally = User.objects.get(username='Sally')
messages.add_message(request, constants_messages.INFO_PERSISTENT, "Hola abc desde %s" %request.user, user=sally)
```

To persistent storages, there are other params like expires that is a datetime.

### Displaying messages ###

Messages can be displayed [as described in the Django manual](http://docs.djangoproject.com/en/dev/ref/contrib/messages/#displaying-messages).
However, you are probably going to want to include links tags for closing each message (i.e.
marking it as read). In your template, use something like:

```htmldjango
{% for message in messages %}
    <div class="alert {% if message.tags %} alert-{{ message.tags }} {% endif %}">
        {# close-href is used because href is used by bootstrap to closing other divs #}
        <a class="close" data-dismiss="alert"{% if message.pk %} close-href="{% url message_mark_read message.pk %}"{% endif %}>×</a>
        {{ message }}
    </div>
{% endfor %}
```

You can also use the bundled templates instead. The following line replaces the code above. It
allows the user to remove messages using [bootstrap styling](http://twitter.github.com/bootstrap/)
(you need use bootstrap.css and boostrap.js)

```htmldjango
{% include "messages_extends/includes/alerts_bootstrap.html" %}
```

For use Ajax to mark them as read you can add the following code that works with jquery:

```javascript
$("a.close[close-href]").click(function (e) {
    e.preventDefault();
    $.post($(this).attr("close-href"), "", function () {
    });
}
);
```

Or use:

```htmldjango
<script src="{% static "close-alerts.js" %}"></script>
```

DON'T FORGET: If you have CSRF enabled, you have to add csrf code by js, [see django Documentation](https://docs.djangoproject.com/en/dev/ref/csrf/#ajax)

If you don't want see close button in sticky alerts, you can use css for hide them:

```css
.alert.sticky .close{
  display: none;
}
```

### Other Backends ###

You can use other backends, by default use:

```python
MESSAGES_STORAGES = ('messages_extends.storages.StickyStorage',
     'messages_extends.storages.PersistentStorage',
     'django.contrib.messages.storage.cookie.CookieStorage',
     'django.contrib.messages.storage.session.SessionStorage'))
```

But you can add or remove other backends in your settings in order that you need execute that,
remember that session storagge save all messages, then you have to put it at final.

### Remember ###
Remember that this module is only for messages from application, to messages between users you can
use [postman](https://bitbucket.org/psam/django-postman) u other framework and to messages for
activity stream you can use [django-activity-stream](https://github.com/justquick/django-activity-stream)


## License ##

Django Messages Extends is provided under [The MIT License (MIT)](http://opensource.org/licenses/MIT).


## Credits ##

Django Messages Extends is a project by [Ali Lozano](mailto:alilozanoc@gmail.com).  Additional credit
goes to:
  * [Steven Klass](sklass@pointcircle.com)


Inspired and based in [django-persistent-messages](https://github.com/samluescher/django-persistent-messages)
