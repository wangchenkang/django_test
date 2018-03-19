# -*- encoding: utf-8 -*-
import json
import datetime
import logging
from django.conf import settings
from django.template.defaultfilters import slugify
import os
import requests


log = logging.getLogger(__name__)


class Storage(object):
    """
    for static file upload to storage
    """

    def __init__(self):
        self.engine = settings.STATIC_SERVER['PUBLIC_API']

    def upload(self, path, file_obj):

        url = self.engine + path
        res = requests.post(url, files={'file': file_obj})
        if res.status_code != 200:
            return False, None
        else:
            return True, res.url
