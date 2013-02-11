# -*- coding: utf-8 -*-
from ospfe.percorso_sla.adapters.mails.mail_base import PercorsoSLAMailBase
from Products.CMFCore.utils import getToolByName

class NotifyDoctor(PercorsoSLAMailBase):
    """
    Classe invio email ai medici. Estende PercorsoSLAMailBase
    """
    
    @property
    def _addresses(self):
        """
        """
        emails = []
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        mt = getToolByName(self.context, 'portal_membership')
        
        readers = self.sla_patient.users_with_local_role('Reader')
        for reader in readers:
            group = portal.acl_users.getGroupById(reader)
            if group:
                emails += [mt.getMemberById(m).getProperty('email') for m in group.getUserIds()]
            else:
                emails.append(mt.getMemberById(reader).getProperty('email'))
        
        return filter(None, list(set(emails)))
