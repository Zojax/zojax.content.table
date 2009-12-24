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
from zope import interface
from zope.i18nmessageid import MessageFactory
from zojax.table.interfaces import ITable, IColumn

_ = MessageFactory('zojax.content.table')


class IContentsTable(ITable):
    """ contents table """


class ITitleColumn(IColumn):
    """ title column """

    showDescription = interface.Attribute('Show content description or not')

    def contentUrl():
        """ return url for current content item """


class ILocationColumn(IColumn):
    """ content location """

    def getLocation():
        """ returns content location """
