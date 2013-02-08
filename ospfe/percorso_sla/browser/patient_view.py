from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

class PatientView(BrowserView):
        
    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
    
    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')
        
    def getSlaFormsPatient(self):
        patient_path = '/'.join(self.context.getPhysicalPath())
        return self.portal_catalog.searchResults(portal_type="sla-form",
                                                 path={'query': patient_path})
        
        

