from plone.indexer.decorator import indexer
from Products.CMFCore.utils import getToolByName
from uwosh.pfg.d2c.interfaces import IFormSaveData2ContentEntry

@indexer(IFormSaveData2ContentEntry)
def color(object, **kw):
    wtool = getToolByName(object, "portal_workflow")
    wf_state = wtool.getInfoFor(object,'review_state')
    if wf_state in ['red','yellow','green']:
        return 'class-%s' % wf_state
    else:
        return ''
        
