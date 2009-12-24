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
from zope.app.pagetemplate import ViewPageTemplateFile

from zojax.table.column import Column
from zojax.content.type.interfaces import IContentType

from interfaces import _, IContentsTable


class TypeColumn(Column):
    component.adapts(interface.Interface, interface.Interface, IContentsTable)

    weight = 25

    name = 'type'
    title = _('Type')
    cssClass = 'ctb-type'
    showName = True

    template = ViewPageTemplateFile('type.pt')

    def query(self, default=None):
        return IContentType(self.content)


class TypeIconColumn(TypeColumn):

    name = 'typeicon'
    cssClass = 'ctb-typeicon'
    showName = False
