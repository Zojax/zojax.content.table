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
from zope import component
from zope.interface import Interface
from zope.traversing.browser import absoluteURL
from zope.app.pagetemplate import ViewPageTemplateFile

from zojax.table.column import Column
from zojax.ownership.interfaces import IOwnership
from zojax.content.table.interfaces import IContentsTable
from zojax.principal.profile.interfaces import IPersonalProfile

from interfaces import _


class AuthorColumn(Column):
    component.adapts(Interface, Interface, IContentsTable)

    weight = 10

    name = 'author'
    title = _('Author')
    cssClass = 'ctb-author'
    showName = True
    showAvatar = True

    template = ViewPageTemplateFile('author.pt')

    def getPrincipal(self, content):
        ownership = IOwnership(self.content, None)
        if ownership is not None:
            return ownership.owner
        return None

    def query(self, default=None):
        principal = self.getPrincipal(self.content)

        if principal is not None:
            request = self.request
            profile = IPersonalProfile(principal)

            info = {'avatar': profile.avatarUrl(request),
                    'title': profile.title,
                    'profile': ''}

            space = profile.space
            if space is not None:
                info['profile'] = '%s/'%absoluteURL(space, request)

            return info


class AvatarColumn(AuthorColumn):
    component.adapts(Interface, Interface, IContentsTable)

    name = 'avatar'
    title = _('Avatar')
    cssClass = 'ctb-avatar'
    showName = False


class AuthorNameColumn(AuthorColumn):
    component.adapts(Interface, Interface, IContentsTable)

    weight = 10

    name = 'authorname'
    title = _('Author')
    cssClass = 'ctb-author'
    showAvatar = False
