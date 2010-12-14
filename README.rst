django-virtualenv-wsgi
======================

**WSGI script for usage in Virtalenvs with Apache - Embedded mod_wsgi**

Features:
---------

- Runs with same settings (sys.path, default language etc.) as the
  Django-built-in dev server
- Guesses source dirs using a glob -- it should run out of the box, without
  the redundancy of ``os.environ['DJANGO_SETTINGS_MODULE']``!
  
Installation:
-------------

Don't bother cloning git repository, unless you're willing to improve this
script in your fork. You can download latest version by simply typing:

``wget https://github.com/hint/django-virtualenv-wsgi/raw/master/django.wsgi``

The git-repo is here: https://github.com/hint/django-virtualenv-wsgi