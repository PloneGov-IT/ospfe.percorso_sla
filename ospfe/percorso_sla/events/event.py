# -*- coding: utf8 -*- 
from ospfe.percorso_sla import logger
from Products.CMFCore.utils import getToolByName

def _setTitleForm(container, form):
    """set title of form"""
    
    _ = getToolByName(container,'translation_service').translate
    title_form = _(msgid='Form of patient',
                   default=u'Form of patient',
                   domain="ospfe.percorso_sla",
                   context=container)
    form.setTitle("%s %s" % (title_form, container.Title()))
    form.reindexObject(idxs=['Title'])

def _createEntry(container, ctype):
    """create an entry of the ctype type in container folder"""
    
    form_id = container.generateUniqueId(ctype)
    container.invokeFactory(id=form_id,type_name=ctype)
    return getattr(container, form_id)

def create_form(object, event):
    """
    Evento alla creazione di un paziente
    """
    form = _createEntry(object, "FormFolder")
    _setTitleForm(object, form)
    
    logger.info('Form creato')