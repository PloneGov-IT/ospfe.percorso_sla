# -*- coding: utf8 -*- 
from ospfe.percorso_sla import logger
from ospfe.percorso_sla.adapters.interfaces import IPercorsoSLAMail
from plone.i18n.normalizer.interfaces import IIDNormalizer
from Products.CMFCore.utils import getToolByName
from zope.component._api import getAdapter
from zope.component import getUtility, queryUtility
from plone.registry.interfaces import IRegistry
from ospfe.percorso_sla.interfaces import ISLAPatientSettings

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
    container.invokeFactory(id=form_id, type_name=ctype)
    return getattr(container, form_id)


def created_patient(obj, event):
    """
    Evento alla creazione di un paziente
    """
    registry = queryUtility(IRegistry)
    settings = registry.forInterface(ISLAPatientSettings, check=False)
    model_patient_path = getattr(settings, 'model_patient', '')
    if model_patient_path:
        portal = obj.portal_url.getPortalObject()
        portal_path = "/".join(portal.getPhysicalPath())
        if not model_patient_path.startswith("/"):
            model_patient_path = "/%s" % model_patient_path
        model_path = portal_path + model_patient_path
        model = portal.restrictedTraverse(str(model_path), None)
        if model:
            copy_from_model(obj, model)
        else:
            create_form(obj)
    else:
        create_form(obj)


def copy_from_model(patient, model):
    """
    Copy default forms from patient model
    """
    model_form_ids = [x.getId() for x in model.listFolderContents(contentFilter={"portal_type": "FormFolder"})]
    forms = model.manage_copyObjects(model_form_ids)
    patient.manage_pasteObjects(forms)
    # copy notification groups from model only if not set
    if not patient.getNotification_groups():
        patient.setNotification_groups(model.getNotification_groups())


def create_form(patient):
    """
    Crea un form di defaul
    """
    form = _createEntry(patient, "FormFolder", '')
    title_adapter = _getTitleAdapter(form)
    adapter = _createEntry(form, "FormSaveData2ContentAdapter", title_adapter)
    adapter.setTitle(title_adapter)
    _configAdapter(adapter)
    adapter.reindexObject()
    _configForm(form, adapter)
    form.reindexObject()

    logger.info('Created form %s with adapter %s' % (form.id, adapter.id))


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
        title_field.set(object, title_sla_form)
        object.reindexObject()


def send_alert(object, event):
    """
    Evento al cambio di stato del form
    """
    wtool = getToolByName(object, "portal_workflow")
    pc = getToolByName(object, "portal_catalog")
    wf_state = wtool.getInfoFor(object, 'review_state')
    parent = object.aq_parent
    same_state_forms = pc(path="/".join(parent.getPhysicalPath()),
                          portal_type=object.portal_type,
                          review_state=wf_state)
    if wf_state in ('red', 'yellow', 'green') and not same_state_forms:
        dc_notification = getAdapter(object, IPercorsoSLAMail, name="notify_doctor")
        dc_notification.send()
        logger.info('Notification to doctors sent')
