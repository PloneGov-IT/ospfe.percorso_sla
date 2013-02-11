# -*- coding: utf-8 -*-
from Acquisition import aq_chain, aq_inner
from email.MIMEText import MIMEText
from email.Utils import parseaddr, formataddr
from ospfe.percorso_sla import logger
from ospfe.percorso_sla.interfaces import ISLAPatient
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode, log_exc
import socket

class PercorsoSLAMailBase(object):
    '''
    Classe Base per un adapter che invia le mail
    '''

    _addresses = None
    _subject = ''
    _text = ''
    
    sla_patient = None

    def __init__(self, context):
        '''
        Verifico se nella catena degli oggetti padre esiste una folder che implementa 
        ISLAPatient.
        @param context: a plone object
        '''
        self.context = context
        self.request = context.REQUEST
        for parent in aq_chain(aq_inner(self.context)):
            if ISLAPatient.providedBy(parent):
                self.sla_patient = parent
                
    @property
    def acl_users(self):
        return getToolByName(self.context, 'acl_users')
    
    @property
    def portal_membership(self):
        return getToolByName(self.context, 'portal_membership')

    @property    
    def translate(self):
        return getToolByName(self.context,'translation_service').translate

    @property    
    def charset(self):
        portal_url = getToolByName(self.context, 'portal_url')
        portal = portal_url.getPortalObject()
        plone_utils = getToolByName(portal, 'plone_utils')
        charset = portal.getProperty('email_charset', '')
        if not charset:
            charset = plone_utils.getSiteEncoding()
        return charset

    def send(self):
        '''
        Send the email
        '''
        if not self.sla_patient:
            logger('Cannot send notification email: no patient found')
            return
        
        self.sendEmail(self._addresses, self._subject, self._text)

    def sendEmail(self, addresses, subject, rstText, cc = None):
        """
        Send a email to the list of addresses
        """
        portal_url  = getToolByName(self.context, 'portal_url')
        plone_utils = getToolByName(self.context, 'plone_utils')
        transforms = getToolByName(self.context, 'portal_transforms')
    
        portal      = portal_url.getPortalObject()
        mailHost    = plone_utils.getMailHost()
        charset     = self.charset
        from_address = portal.getProperty('email_from_address', '')
    
        if not from_address:
            logger('Cannot send notification email: email sender address not set')
            return
        from_name = portal.getProperty('email_from_name', '')
        mfrom = formataddr((from_name, from_address))
        if parseaddr(mfrom)[1] != from_address:
            # formataddr probably got confused by special characters.
            mfrom - from_address

        # We must choose the body charset manually
        for body_charset in (charset, 'UTF-8', 'US-ASCII'):
            try:
                rstText = rstText.encode(body_charset)
            except UnicodeError:
                pass
            else:
                break
        
        email_msg = MIMEText(rstText, 'plain', body_charset)
    
        subject = safe_unicode(subject, charset)
    
        for address in addresses:
            address = safe_unicode(address, charset)
            if address:
                try:
                    # Note that charset is only used for the headers, not
                    # for the body text as that is a Message already.
                    mailHost.secureSend(message = email_msg,
                                        mto = address,
                                        mfrom = mfrom,
                                        subject = subject,
                                        charset = charset)
                except socket.error, exc:
                    log_exc(('Could not send email from %s to %s regarding issue '
                             'in content %s\ntext is:\n%s\n') % (
                            mfrom, address, self.context.absolute_url(), email_msg))
                    log_exc("Reason: %s: %r" % (exc.__class__.__name__, str(exc)))
                except:
                    raise
