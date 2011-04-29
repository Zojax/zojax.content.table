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
from zojax.content.type.interfaces import IContentContainer
from zojax.catalog.interfaces import ICatalog
"""

$Id$
"""
from zope import component, interface
from zope.component import queryMultiAdapter, getUtility
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
    
    def update(self):
        super(ModifiedColumn, self).update()
        self.catalog = getUtility(ICatalog)

    def query(self, default=None):
        dc = None
        if IContentContainer.providedBy(self.content):
            try:
                dc = IDCTimes(self.catalog.searchResults(traversablePath={'any_of':(self.content,)},
                                                         sort_on='modified', sort_order='reverse')[0], None)
            except (TypeError,IndexError), e:
                pass
        if dc is None:
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
