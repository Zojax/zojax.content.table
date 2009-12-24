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

from interfaces import _, IContentsTable, ITitleColumn


class TitleColumn(Column):
    interface.implementsOnly(ITitleColumn)
    component.adapts(interface.Interface, interface.Interface, IContentsTable)

    weight = 20

    name = 'title'
    title = _('Title')
    cssClass = 'ctb-title'
    showDescription = False

    template = ViewPageTemplateFile('title.pt')

    def query(self, default=None):
        item = IItem(self.content, None)

        title = u''
        description = u''
        if item is not None:
            title = item.title
            description = item.description

        return {'url': self.contentUrl(),
                'title': title or _('[No title]'),
                'content': self.content,
                'description': description or u''}

    def contentUrl(self):
        content = self.content
        request = self.request

        view = queryMultiAdapter((content, request), IContentViewView)
        if view is not None:
            url = '%s/%s'%(absoluteURL(content, request), view.name)
        else:
            url = '%s/'%absoluteURL(content, request)

        return url


class TitleWithDescriptionColumn(TitleColumn):

    showDescription = True
