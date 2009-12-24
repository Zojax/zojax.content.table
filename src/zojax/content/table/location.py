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
from zope.traversing.browser import absoluteURL
from zope.app.pagetemplate import ViewPageTemplateFile

from zojax.table.column import Column
from zojax.content.type.interfaces import IItem, IContentViewView
from zojax.content.table.interfaces import _, ILocationColumn, IContentsTable


class LocationColumn(Column):
    interface.implementsOnly(ILocationColumn)
    component.adapts(interface.Interface, interface.Interface, IContentsTable)

    weight = 50

    name = 'location'
    title = _('Location')
    cssClass = 'ctb-location'
    template = ViewPageTemplateFile('location.pt')

    def getLocation(self):
        return self.content.__parent__

    def query(self, default=None):
        request = self.request
        content = self.getLocation()
        if content is None:
            return

        item = IItem(content, None)

        title = u''
        description = u''
        if item is not None:
            title = item.title
            description = item.description

        view = queryMultiAdapter((content, request), IContentViewView)
        if view is not None:
            url = '%s/%s'%(absoluteURL(content, request), view.name)
        else:
            url = '%s/'%absoluteURL(content, request)

        return {'url': url,
                'title': title or _('[No title]'),
                'content': content,
                'icon': queryMultiAdapter((content, request), name='zmi_icon'),
                'description': description or u''}
