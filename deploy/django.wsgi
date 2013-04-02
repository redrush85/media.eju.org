#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os, sys
sys.path.append('/home/django-projects')
sys.path.append('/home/django-projects/ejumedia')

os.environ['DJANGO_SETTINGS_MODULE'] = 'ejumedia.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()