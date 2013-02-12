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
                                                 path={'query': patient_path})
        
    def getFormsFolderPatient(self):
        patient_path = '/'.join(self.context.getPhysicalPath())
        return self.portal_catalog.searchResults(portal_type="FormFolder",
                                                 path={'query': patient_path})
        
    def check_user_can_fill_form(self):
        portal_membership = getToolByName(self.context, 'portal_membership')
        member = portal_membership.getAuthenticatedMember()
        if not member:
            return False
        
        site = getSite()
        rolesOfperm = site.rolesOfPermission("uwosh.pfg.d2c: Add FormSaveData2ContentEntry")
        rolesIncontext = member.getRolesInContext(self.context)
        
        found = False
        
        for role in rolesOfperm:
            if role["selected"] != "": # will be SELECTED if the permission is granted
                if role["name"] in rolesIncontext:
                    found = True
                    break
        
        return found
        
#        from AccessControl import getSecurityManager
#        sm = getSecurityManager()
#        if sm.checkPermission("uwosh.pfg.d2c: Add FormSaveData2ContentEntry", self.context):
#            return True
#        else:
#            return False
        
        

