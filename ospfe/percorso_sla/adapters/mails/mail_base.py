# -*- coding: utf-8 -*-
from Acquisition import aq_chain, aq_inner
from email.MIMEMultipart import MIMEMultipart
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
        charset     = portal.getProperty('email_charset', '')
        if not charset:
            charset = plone_utils.getSiteEncoding()
        from_address = portal.getProperty('email_from_address', '')
    
        if not from_address:
            logger('Cannot send notification email: email sender address not set')
            return
        from_name = portal.getProperty('email_from_name', '')
        mfrom = formataddr((from_name, from_address))
        if parseaddr(mfrom)[1] != from_address:
            # formataddr probably got confused by special characters.
            mfrom - from_address
    
        email_msg = MIMEMultipart('alternative')
        email_msg.epilogue = ''
    
        translate = getToolByName(self.context,'translation_service').translate
    
        # We must choose the body charset manually
        for body_charset in (charset, 'UTF-8', 'US-ASCII'):
            try:
                rstText = rstText.encode(body_charset)
            except UnicodeError:
                pass
            else:
                break
    
        # Text came from HTML text fields inside adapter, so I will convert it to simple text 
        stream = transforms.convertTo('text/plain', rstText, mimetype='text/html')
        textPart = MIMEText(stream.getData().strip(), 'plain', body_charset)
        email_msg.attach(textPart)
        htmlPart = MIMEText(renderHTML(rstText, charset=body_charset),
                            'html', body_charset)
        email_msg.attach(htmlPart)
    
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

def renderHTML(rstText, lang='en', charset='utf-8'):
    """Convert the given rST into a full XHTML transitional document.
    """

    kwargs = {'lang': lang,
              'charset': charset,
              'body': rstText}
    
    return htmlTemplate % kwargs

htmlTemplate = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"
      xml:lang="%(lang)s"
      lang="%(lang)s">

  <head>
     <meta http-equiv="Content-Type" content="text/html; charset=%(charset)s" />

    <style type="text/css" media="all">
<!--
body {
    font-size: 0.9em;
}

h4 {
    font-size: 1.2em;
    font-weight: bold;
}

dt {
    font-weight: bold;
}
-->
    </style>

  </head>

  <body>
%(body)s
  </body>
</html>
"""