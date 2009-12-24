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
""" zojax.content.table tests

$Id$
"""
import os, unittest, doctest
from zope import interface, component, schema
from zope.app.testing import functional
from zope.app.component.hooks import setSite
from zojax.ownership.interfaces import IOwnerAware
from zojax.content.type.item import IItem, PersistentItem
from zojax.content.type.container import ContentContainer
from zojax.content.type.interfaces import IContentViewView


zojaxContentTableLayer = functional.ZCMLLayer(
    os.path.join(os.path.split(__file__)[0], 'ftesting.zcml'),
    __name__, 'zojaxContentTableLayer', allow_teardown=True)


class IDocument(IItem):

    text = schema.Text(
        title = u'Text',
        required = False)


class Document(PersistentItem):
    interface.implements(IDocument, IOwnerAware)


class DocumentView(object):
    component.adapts(IDocument, interface.Interface)
    interface.implements(IContentViewView)

    name = 'view.html'
    def __init__(self, doc, request):
        pass

class IDocumentContainer(IItem):
    pass


class DocumentContainer(ContentContainer):
    interface.implements(IDocumentContainer)


def FunctionalDocFileSuite(*paths, **kw):
    layer = zojaxContentTableLayer

    globs = kw.setdefault('globs', {})
    globs['http'] = functional.HTTPCaller()
    globs['getRootFolder'] = functional.getRootFolder
    globs['sync'] = functional.sync

    kw['package'] = doctest._normalize_module(kw.get('package'))

    kwsetUp = kw.get('setUp')
    def setUp(test):
        functional.FunctionalTestSetup().setUp()

    kw['setUp'] = setUp

    kwtearDown = kw.get('tearDown')
    def tearDown(test):
        setSite(None)
        functional.FunctionalTestSetup().tearDown()

    kw['tearDown'] = tearDown

    if 'optionflags' not in kw:
        old = doctest.set_unittest_reportflags(0)
        doctest.set_unittest_reportflags(old)
        kw['optionflags'] = (old|doctest.ELLIPSIS|doctest.NORMALIZE_WHITESPACE)

    suite = doctest.DocFileSuite(*paths, **kw)
    suite.layer = layer
    return suite


def test_suite():
    return unittest.TestSuite((
            FunctionalDocFileSuite("testbrowser.txt"),
            ))
