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
    
    def get_authenticated_member_email(self):
        mt = getToolByName(self.context, 'portal_membership')
        authenticated_member = mt.getAuthenticatedMember()
        if authenticated_member:
            return authenticated_member.getProperty('email')
        return ''
    
    @property
    def _addresses(self):
        """
        """
        readers      = self.sla_patient.users_with_local_role('Reader')
        contributors = self.sla_patient.users_with_local_role('Contributor')
        emails = self.get_emails(readers) + self.get_emails(contributors)
        
        self.get_authenticated_member_email()
        
        return filter(None, list(set(emails)))
