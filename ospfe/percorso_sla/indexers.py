from plone.indexer.decorator import indexer
from uwosh.pfg.d2c.interfaces import IFormSaveData2ContentEntry

@indexer(IFormSaveData2ContentEntry)
def color(object, **kw):
    return 'red'