# ~*~ coding: utf-8 ~*~
from __future__ import unicode_literals, absolute_import

import logging
import json

from django.db import models
from django.utils.translation import ugettext_lazy as _


logger = logging.getLogger(__name__)


class AnsiblePlay(models.Model):
    uuid = models.CharField(max_length=128, verbose_name=_('UUID'), primary_key=True)
    name = models.CharField(max_length=128, verbose_name=_('Name'))
    completed = models.BooleanField(default=False, verbose_name=_('IsCompleted'))
    status_code = models.IntegerField(default=0, verbose_name=_('StatusCode'))

    def __unicode__(self):
        return "AnsiblePlay: %s<%s>" % (self.name, self.uuid)


class AnsibleTask(models.Model):
    uuid = models.CharField(max_length=128, verbose_name=_('UUID'), primary_key=True)
    play = models.ForeignKey(AnsiblePlay, related_name='tasks', blank=True)
    name = models.CharField(max_length=128, blank=True, verbose_name=_('Name'))

    def __unicode__(self):
        return "AnsibleTask: %s<%s>" % (self.name, self.uuid)

    def failed(self):
        pass

    def success(self):
        pass


class AnsibleHostResult(models.Model):
    task = models.ForeignKey(AnsibleTask, related_name='host_results', blank=True)
    name = models.CharField(max_length=128, blank=True, verbose_name=_('Name'))
    status = models.BooleanField(blank=True, default=False, verbose_name=_('Status'))
    success = models.TextField(blank=True, verbose_name=_('Success'))
    skipped = models.TextField(blank=True, verbose_name=_('Skipped'))
    failed = models.TextField(blank=True, verbose_name=_('Failed'))
    unreachable = models.TextField(blank=True, verbose_name=_('Unreachable'))
    no_host = models.TextField(blank=True, verbose_name=_('NoHost'))

    def __unicode__(self):
        return "AnsibleHostResult: %s<%s>" % (self.name, str(self.status))

    @property
    def is_failed(self):
        if self.failed or self.unreachable or self.no_host:
            return True
        return False

    @property
    def success_data(self):
        if self.success:
            return json.loads(self.success)
        elif self.skipped:
            return json.loads(self.skipped)

    @property
    def failed_data(self):
        if self.failed:
            return json.loads(self.failed)
        elif self.unreachable:
            return json.loads(self.unreachable)
        elif self.no_host:
            return {"msg": self.no_host}

