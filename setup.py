import os
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-persistent-messages',
    version='0.1',
    description='A Django app for unified and persistent user messages/notifications, built on top of Django\'s messages framework',
    long_description=read('README.md'),
    author='philomat',
    license='BSD',
    url='http://github.com/philomat/django-persistent-messages',
    keywords = ['messages', 'django', 'persistent',],
    packages=[
        'persistent_messages',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    zip_safe=False,
)
