# -*- coding: utf-8 -*-
from ospfe.percorso_sla.adapters.mails.mail_base import PercorsoSLAMailBase
from Products.CMFCore.utils import getToolByName

class NotifyDoctor(PercorsoSLAMailBase):
    """
    Classe invio email ai medici. Estende PercorsoSLAMailBase
    """
    
    def get_emails(self, users):
        emails = []
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        mt = getToolByName(self.context, 'portal_membership')
        for user in users:
            group = portal.acl_users.getGroupById(user)
            if group:
                emails += [mt.getMemberById(m).getProperty('email') for m in group.getUserIds()]
            else:
                emails.append(mt.getMemberById(user).getProperty('email'))
        return emails
    
    @property
    def _addresses(self):
        """
        """
        readers = self.sla_patient.users_with_local_role('Reader')
        readers_emails = self.get_emails(readers)
        emails = readers_emails
        
        return filter(None, list(set(emails)))
