# -*- coding: utf-8 -*-

from Products.statusmessages.interfaces import IStatusMessage

from plone.app.registry.browser import controlpanel

from z3c.form import button
from z3c.form import field

from ospfe.percorso_sla.interfaces import ISLAPatientSettings
from ospfe.percorso_sla import percorso_slaMessageFactory as _


class SLAPatientSettingsEditForm(controlpanel.RegistryEditForm):
    """
    Settings form.
    """
    schema = ISLAPatientSettings
    fields = field.Fields(ISLAPatientSettings)
    id = "SLAPatientSettingsEditForm"
    label = _(u"SLA Patient settings")
    description = _(u"help_slapatient_settings_editform",
                    default=u"Set SLA patient configurations")

    @button.buttonAndHandler(_('Save'), name='save')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        changes = self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage(_(u"Changes saved"),
                                                      "info")
        self.context.REQUEST.RESPONSE.redirect("@@sla-settings")

    @button.buttonAndHandler(_('Cancel'), name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(_(u"Edit cancelled"),
                                                      "info")
        self.request.response.redirect("%s/%s" % (self.context.absolute_url(),
                                                  self.control_panel_view))


class SLAPatientSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    """SLA patient settings control panel.
    """
    form = SLAPatientSettingsEditForm
