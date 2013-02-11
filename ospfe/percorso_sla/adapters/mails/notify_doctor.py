# -*- coding: utf-8 -*-
from ospfe.percorso_sla.adapters.mails.mail_base import PercorsoSLAMailBase
from Products.CMFCore.utils import getToolByName

class NotifyDoctor(PercorsoSLAMailBase):
    """
    Classe invio email ai medici. Estende PercorsoSLAMailBase
    """
    
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
