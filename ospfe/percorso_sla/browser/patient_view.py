from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

class PatientView(BrowserView):
        
    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)

