# -*- coding: utf8 -*- 
from ospfe.percorso_sla import logger


def _createEntry(container, ctype):
    "create an entry of the ctype type in container folder"
    
    form_id = container.generateUniqueId(ctype)
    container.invokeFactory(id=form_id,type_name=ctype)
    return getattr(container, form_id)

def create_form(object, event):
    """
    Evento alla creazione di un paziente
    """
    form = _createEntry(object, "FormFolder")    
    logger.info('Form creato')