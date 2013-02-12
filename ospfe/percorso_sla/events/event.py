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
    form.setThanksPage('')
    # titolo campo nascosto
    title_sla_form = _createEntry(form, 'FormStringField', 'Title SLA Form')
    title_sla_form.setTitle('Title')
    title_sla_form.setHidden(True)
    title_sla_form.reindexObject()

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
    return _(msgid='Adapter save form patient',
             default=u'Adapter save form patient',
             domain="ospfe.percorso_sla",
             context=container)

def _setTitleAdapter(title_adapter, adapter):
    """set title of adapter"""
    
    adapter.setTitle(title_adapter)
    
def _getTitleForm(container):
    """get title of form"""
    
    _ = getToolByName(container,'translation_service').translate
    title_form = _(msgid='Form of patient',
                   default=u'Form of patient',
                   domain="ospfe.percorso_sla",
                   context=container)
    return "%s %s" % (title_form, container.Title())

def _setTitleForm(title_form, form):
    """set title of form"""
    
    form.setTitle(title_form)

def _createEntry(container, ctype, title):
    """create an entry of the ctype type in container folder"""
    normalizer = getUtility(IIDNormalizer)
    form_id = normalizer.normalize(title)
    container.invokeFactory(id=form_id,type_name=ctype)
    return getattr(container, form_id)

def create_form(object, event):
    """
    Evento alla creazione di un paziente
    """
    title_form = _getTitleForm(object)
    form = _createEntry(object, "FormFolder", title_form)
    _setTitleForm(title_form, form)
    
    title_adapter = _getTitleAdapter(form)
    adapter = _createEntry(form, "FormSaveData2ContentAdapter", title_adapter)
    _setTitleAdapter(title_adapter, adapter)
    _configAdapter(adapter)
    adapter.reindexObject()
    
    _configForm(form,adapter)
    form.reindexObject()
    
    logger.info('Created form %s with adapter %s' % (form.id,adapter.id))
    
def create_sla_form(object, event):
    """
    Evento alla creazione di una scheda SLA: impostiamo titolo
    """
    title_sla_form = '%s %s' % (object.aq_inner.aq_parent.aq_parent.Title(),object.created().strftime('%d/%m/%Y'))
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
