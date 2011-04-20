django-virtualenv-wsgi
======================

Django WSGI handler setting up a proper environment based on Virtualenv,
with possible server maintenance message (503 Service Unavailable) responding.

Usage
-----

Default project tree should look like::

    some_project
    |- _env/
    |- django_project/
    |- django.wsgi
    |- maintenance.html
    |- maintenance.lock

* ``_env/``
  virtualenv environment directory
* ``django_project/``
  django project package directory
* ``django.wsgi``
  a django.wsgi file from this package
* ``maintenance.html``
  a HTML file (UTF-8 encoded) with which server will respond in maintenance mode
* ``maintenance.lock``
  maintenance mode lock -- see below

You must make sure that your Django project directory name is same as in a ``django.wsgi``'s
``PROJECT_NAME`` setting.

Maintenance mode
----------------

To enable maintenance mode just create a ``maintenance.lock`` file in the same directory
``django.wsgi`` is located, and tell your server to reload the WSGI handler. You can do
all of this with a simple line::

    $ touch maintenance.lock ; touch django.wsgi

To disable maintenance mode just remove ``maintenance.lock`` and reload the handler::

    $ rm maintenance.lock ; touch django.wsgi

In case ``maintenance.html`` doesn't exist server will respond with default plain text message
(you can change it with ``django.wsgi``'s ``MAINTENANCE_MESSAGE_FALLBACK`` setting). 

