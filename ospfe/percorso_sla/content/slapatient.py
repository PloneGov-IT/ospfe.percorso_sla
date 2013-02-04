"""Definition of the SLA Patient content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.Archetypes.atapi import AnnotationStorage
from Products.Archetypes.atapi import RichWidget
from Products.Archetypes.atapi import TextField
from Products.ATContentTypes import ATCTMessageFactory
from Products.ATContentTypes.configuration import zconf
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata

# -*- Message Factory Imported Here -*-

from ospfe.percorso_sla.interfaces import ISLAPatient
from ospfe.percorso_sla.config import PROJECTNAME

from ospfe.percorso_sla import percorso_slaMessageFactory as _

SLAPatientSchema = folder.ATFolderSchema.copy() + atapi.Schema((

    TextField('text',
          required=False,
          searchable=True,
          primary=True,
          storage = AnnotationStorage(migrate=True),
          validators = ('isTidyHtmlWithCleanup',),
          #validators = ('isTidyHtml',),
          default_output_type = 'text/x-html-safe',
          widget = RichWidget(
                    description = '',
                    label = ATCTMessageFactory(u'label_body_text', default=u'Body Text'),
                    rows = 25,
                    allow_file_upload = zconf.ATDocument.allow_document_upload),
    ),

))

# Set storage on fields copied from ATFolderSchema, making sure
# they work well with the python bridge properties.

SLAPatientSchema['title'].storage = atapi.AnnotationStorage()
SLAPatientSchema['description'].storage = atapi.AnnotationStorage()
SLAPatientSchema['title'].widget.label = _(u'label_title', default=u'Patient name')

schemata.finalizeATCTSchema(
    SLAPatientSchema,
    folderish=True,
    moveDiscussion=False
)


class SLAPatient(folder.ATFolder):
    """Description of the Example Type"""
    implements(ISLAPatient)

    meta_type = "SLAPatient"
    schema = SLAPatientSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')

    # -*- Your ATSchema to Python Property Bridges Here ... -*-

atapi.registerType(SLAPatient, PROJECTNAME)