from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from zope.app.component.hooks import getSite

class PatientView(BrowserView):
        
    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
    
    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')
        
    def getSlaFormsPatient(self):
        patient_path = '/'.join(self.context.getPhysicalPath())
        return self.portal_catalog.searchResults(portal_type="sla-form",
                                                 path={'query': patient_path},
                                                 sort_on='created', sort_order='reverse')
        
    def getFormsFolderPatient(self):
        patient_path = '/'.join(self.context.getPhysicalPath())
        return self.portal_catalog.searchResults(portal_type="FormFolder",
                                                 path={'query': patient_path},
                                                 sort_on='sortable_title', sort_order='ascending')
        
    def check_user_can_fill_form(self, content):
        portal_membership = getToolByName(self.context, 'portal_membership')
        member = portal_membership.getAuthenticatedMember()
        if not member:
            return False
        return portal_membership.checkPermission("uwosh.pfg.d2c: Add FormSaveData2ContentEntry",
                                                 content.getObject())