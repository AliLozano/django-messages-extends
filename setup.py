import os
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-messages-extends',
    version='0.1',
    description='A Django app for extends Django\'s messages framework, adds sticky messages and persistent messages',
    long_description=read('README.md'),
    author='philomat',
    #base-project = 'https://github.com/philomat/django-persistent-messages',
    co-author='AliLozano',
    license='BSD',
    url='https://github.com/AliLozano/django-messages-extends/',
    keywords=['messages', 'django', 'persistent', 'sticky',  ],
    packages=[
        'messages_extends',
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
