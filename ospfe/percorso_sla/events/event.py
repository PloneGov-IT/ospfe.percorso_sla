# -*- coding: utf8 -*- 
from ospfe.percorso_sla import logger
from ospfe.percorso_sla.adapters.interfaces import IPercorsoSLAMail
from plone.i18n.normalizer.interfaces import IIDNormalizer
from Products.CMFCore.utils import getToolByName
from zope.component._api import getAdapter
from zope.component import getUtility

def _configForm(form, adapter):
    """configuration of form"""
    _ = getToolByName(form,'translation_service').translate
    form.setSubmitLabel(_(msgid='Submit',
                          default=u'Submit',
                          domain="ospfe.percorso_sla",
                          context=form))
    form.setUseCancelButton(True)
    form.setActionAdapter((adapter.id))
    # titolo campo nascosto
    title_sla_form = _createEntry(form, 'FormStringField', 'Title SLA Form')
    title_sla_form.setTitle('Title')
    title_sla_form.setHidden(True)
    title_sla_form.reindexObject()
    # elimina i mailer adapters
    mailers = form.listFolderContents(contentFilter={"portal_type" : "FormMailerAdapter"})
    for mailer in mailers:
        form.manage_delObjects([mailer.id])

def _configAdapter(adapter):
    """configuration of adapter"""
    adapter.setAvoidSecurityChecks(False)
    adapter.setEntryType('sla-form')
    adapter.setNiceIds(True)
    adapter.setTitleField('title-sla-form')
    #adapter.setDynamicTitle("python: '%s %s' % (here.aq_inner.aq_parent.aq_parent.Title(),here.created().strftime('%d/%m/%Y'))")

def _getTitleAdapter(container):
    """get title of adapter"""
    
    _ = getToolByName(container,'translation_service').translate
    return _(msgid='Forms of patient',
             default=u'Forms of patient',
             domain="ospfe.percorso_sla",
             context=container)

def _createEntry(container, ctype, title):
    """create an entry of the ctype type in container folder"""
    normalizer = getUtility(IIDNormalizer)
    if title:
        form_id = normalizer.normalize(title)
    else:
        form_id = container.generateUniqueId(ctype)
    container.invokeFactory(id=form_id,type_name=ctype)
    return getattr(container, form_id)

def create_form(object, event):
    """
    Evento alla creazione di un paziente
    """
    form = _createEntry(object, "FormFolder", '')
    title_adapter = _getTitleAdapter(form)
    adapter = _createEntry(form, "FormSaveData2ContentAdapter", title_adapter)
    adapter.setTitle(title_adapter)
    _configAdapter(adapter)
    adapter.reindexObject()
    
    _configForm(form,adapter)
    form.reindexObject()
    
    logger.info('Created form %s with adapter %s' % (form.id,adapter.id))
    
def create_sla_form(object, event):
    """
    Evento alla creazione di una scheda SLA: impostiamo titolo
    """
    container = object.aq_inner.aq_parent
    title_sla_form = '%s - %s (%s)' % (container.aq_parent.aq_parent.Title(),
                                       container.aq_parent.Title(),
                                       object.created().strftime('%d/%m/%Y'))
    title_field = object.getField('title-sla-form')
    if title_field:
        title_field.set(object,title_sla_form)
        object.reindexObject()
    
def send_alert(object, event):
    """
    Evento al cambio di stato del form
    """
    wtool = getToolByName(object, "portal_workflow")
    wf_state = wtool.getInfoFor(object,'review_state')
    if not wf_state == "red":
        return

    dc_notification = getAdapter(object, IPercorsoSLAMail, name="notify_doctor")
    dc_notification.send()
    logger.info('Notification to doctors sent')
