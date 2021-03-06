# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode

from ospfe.percorso_sla.adapters.mails.mail_base import PercorsoSLAMailBase

class NotifyDoctor(PercorsoSLAMailBase):
    """
    Classe invio email ai medici. Estende PercorsoSLAMailBase
    """

    def su(self, value):
        return safe_unicode(value, encoding=self.charset)

    def get_emails(self, users):
        emails = []
        for user in users:
            group = self.acl_users.getGroupById(user) or self.acl_users.getGroupByName(user)
            if group:
                emails += [member.getProperty('email')
                           for member in group.getAllGroupMembers()
                           if (member and member.getProperty('email'))]
            else:
                member = self.portal_membership.getMemberById(user)
                if member and member.getProperty('email'):
                    emails.append(member.getProperty('email'))
        return emails
    
    @property
    def _addresses(self):
        """
        """
        notification_groups = self.sla_patient.getNotification_groups()
        emails = self.get_emails(notification_groups)
        return filter(None, list(set(emails)))
    
    @property
    def _subject(self):
        _ = self.translate

        return _(msgid='subject_notify_doctor',
                 default=u'[SLA Form] - SLA Form in state "${review_state}"',
                 domain="ospfe.percorso_sla",
                 context=self.context,
                 mapping={'review_state': self.su(self.translate(self.slaform_review_state, domain="plone"))},
                )
    
    @property
    def slaformCreator(self):
        slaformCreator = self.context.Creator()
        slaformCreatorInfo = self.portal_membership.getMemberInfo(slaformCreator)
        slaformAuthor = slaformCreator
        if slaformCreatorInfo:
            slaformAuthor = slaformCreatorInfo['fullname'] or slaformCreator
        return slaformAuthor

    @property
    def slaform_review_state(self):
        wtool = getToolByName(self.context, 'portal_workflow')
        review_state = wtool.getInfoFor(self.context, 'review_state')
        if review_state:
            return review_state.title()

    @property        
    def _text(self):
        _ = self.translate
        
        mapping = dict(sla_form_title = self.su(self.context.title_or_id()),
                       sla_form_creation_date = self.su(self.context.toLocalizedTime(self.context.created())),
                       sla_form_owner = self.su(self.slaformCreator),
                       review_state = self.su(self.translate(self.slaform_review_state, domain="plone")),
                       patient = self.su(self.sla_patient.title_or_id()),
                       sla_form_url = self.su(self.context.absolute_url()),
                       )
        
        return _(msgid='mail_text_notify_doctor', default=u"""Dear user,

this is a personal communication regarding the SLA Form ${sla_form_title}, created on ${sla_form_creation_date} by ${sla_form_owner}.

The SLA Form of patient ${patient} is in state "${review_state}". Follow the link below for visit the SLA form:

${sla_form_url}

Regards""", domain="ospfe.percorso_sla", context=self.context, mapping=mapping)
