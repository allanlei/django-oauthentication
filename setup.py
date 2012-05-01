from distutils.core import setup
from setuptools import find_packages
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def find_packages_in(where, **kwargs):
    return [where] + ['%s.%s' % (where, package) for package in find_packages(where=where, **kwargs)]

setup(
    name = 'django-oauthentication',
    version = '0.1.0',
    author = 'Allan Lei',
    author_email = 'allanlei@helveticode.com',
    description = 'OAuth 2.0 authentication for Django',
    long_description=open('README.md').read(),
    license=open('LICENSE.txt').read(),
    keywords = 'django auth oauth2.0',
    url = 'https://github.com/allanlei/django-oauthentication',
    packages=find_packages_in('oauth2'),
    install_requires=[
        'django-appconf==0.4.1',
        'requests==0.11.1',
    ],
)
