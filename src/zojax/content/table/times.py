##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
from zope import component, interface
from zope.component import queryMultiAdapter
from zope.dublincore.interfaces import IDCTimes

from zojax.table.column import Column
from zojax.formatter.utils import getFormatter

from interfaces import _, IContentsTable


class TimesColumn(Column):
    component.adapts(interface.Interface, interface.Interface, IContentsTable)

    weight = 50

    def update(self):
        super(TimesColumn, self).update()

        self.table.environ['humanDatetime'] = getFormatter(
            self.request, 'humanDatetime', 'medium')

    def render(self):
        value = self.query()
        if value:
            return self.globalenviron['humanDatetime'].format(value)

        return u'---'


class ModifiedColumn(TimesColumn):

    name = 'modified'
    title = _('Last updated')
    cssClass = 'ctb-modified'

    def query(self, default=None):
        dc = IDCTimes(self.content, None)
        if dc is not None:
            return dc.modified

        return None


class CreatedColumn(TimesColumn):

    name = 'created'
    title = _('Created')
    cssClass = 'ctb-created'

    def query(self, default=None):
        dc = IDCTimes(self.content, None)
        if dc is not None:
            return dc.created

        return None
